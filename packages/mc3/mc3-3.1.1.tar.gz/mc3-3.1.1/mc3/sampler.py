class sampler():
    def __init__(
        self, data=None, uncert=None, func=None, params=None, indparams=[],
        pmin=None, pmax=None, pstep=None,
        prior=None, priorlow=None, priorup=None,
        sampler=None, ncpu=None, leastsq=None, chisqscale=False,
        nchains=7, nsamples=None, burnin=0, thinning=1,
        grtest=True, grbreak=0.0, grnmin=0.5, wlike=False,
        fgamma=1.0, fepsilon=0.0, hsize=10, kickoff='normal',
        plots=False, ioff=False, showbp=True, savefile=None, resume=False,
        rms=False, log=None, pnames=None, texnames=None,
        **kwargs,
    ):
        # Logging object:
        if isinstance(log, str):
            self.log = mu.Log(log, append=resume)
            self._closelog = True
        else:
            if log is None:
                self.log = mu.Log()
            else:
                self.log = log
            self._closelog = False

        log.msg(
           f"\n{log.sep}\n"
            "  Multi-core Markov-chain Monte Carlo (mc3).\n"
           f"  Version {__version__}.\n"
           f"  Copyright (c) 2015-{date.today().year} Patricio Cubillos "
              "and collaborators.\n"
            "  mc3 is open-source software under the MIT license (see LICENSE).\n"
           f"{log.sep}\n\n")

        if sampler is None:
            log.error("'sampler' is a required argument")
        if nsamples is None and sampler in ['MRW', 'DEMC', 'snooker']:
            log.error("'nsamples' is a required argument for MCMC runs")
        if leastsq not in [None, 'lm', 'trf']:
            log.error(
                f"Invalid 'leastsq' input ({leastsq}). Must select from "
                 "['lm', 'trf']")

        # Read the model parameters:
        params = mu.isfile(params, 'params', log, 'ascii', False, not_none=True)
        # Unpack if necessary:
        if np.ndim(params) > 1:
            ninfo, ndata = np.shape(params)
            if ninfo == 7:         # The priors
                prior = params[4]
                priorlow = params[5]
                priorup = params[6]
            if ninfo >= 4:         # The stepsize
                pstep = params[3]
            if ninfo >= 3:         # The boundaries
                pmin = params[1]
                pmax = params[2]
            else:
                log.error('Invalid format/shape for params input file')
            params = params[0]     # The initial guess
        params = np.array(params)


        # Process data and uncertainties:
        data = mu.isfile(data, 'data', log, 'bin', False, not_none=True)
        if np.ndim(data) > 1:
            data, uncert = data
        # Make local 'uncert' a copy, to avoid overwriting:
        if uncert is None:
            log.error("'uncert' is a required argument")
        uncert = np.copy(uncert)

        # Process the independent parameters:
        if indparams != []:
            indparams = mu.isfile(indparams, 'indparams', log, 'bin', unpack=False)

        if ioff:
            plt.ioff()

        resume = resume and (savefile is not None)
        if resume:
            log.msg(f"\n\n{log.sep}\n{log.sep}  Resuming previous MCMC run.\n\n")

        # Import the model function:
        if isinstance(func, (list, tuple, np.ndarray)):
            if len(func) == 3:
                sys.path.append(func[2])
            else:
                sys.path.append(os.getcwd())
            fmodule = importlib.import_module(func[1])
            func = getattr(fmodule, func[0])
        elif not callable(func):
            log.error(
                "'func' must be either a callable or an iterable of strings "
                "with the model function, file, and path names")


        if ncpu is None and sampler in ['snooker', 'demc', 'mrw']:
            ncpu = nchains
        elif ncpu is None and sampler == 'dynesty':
            ncpu = 1
        # Cap the number of processors:
        if ncpu >= mpr.cpu_count():
            log.warning(
                f"The number of requested CPUs ({ncpu}) is >= than the number "
                f"of available CPUs ({mpr.cpu_count()}).  "
                f"Enforced ncpu to {mpr.cpu_count()-1}.")
            ncpu = mpr.cpu_count() - 1

        nparams = len(params)
        ndata = len(data)

        # Setup array of parameter names:
        if pnames is None and texnames is not None:
            pnames = texnames
        elif pnames is not None and texnames is None:
            texnames = pnames
        elif pnames is None and texnames is None:
            pnames = texnames = mu.default_parnames(nparams)
        pnames = np.asarray(pnames)
        texnames = np.asarray(texnames)

        if pmin is None:
            pmin = np.tile(-np.inf, nparams)
        if pmax is None:
            pmax = np.tile( np.inf, nparams)
        pmin = np.asarray(pmin)
        pmax = np.asarray(pmax)
        if (np.any(np.isinf(pmin)) or np.any(np.isinf(pmax))) \
                and sampler=='dynesty':
            log.error('Parameter space must be constrained by pmin and pmax')

        if pstep is None:
            pstep = 0.1 * np.abs(params)
        pstep = np.asarray(pstep)


        # Set prior parameter indices:
        if prior is None or priorup is None or priorlow is None:
            prior = priorup = priorlow = np.zeros(nparams)

        # Override priors for non-free parameters:
        priorlow[pstep<=0] = 0.0
        priorup [pstep<=0] = 0.0

        # Check that initial values lie within the boundaries:
        if np.any(params < pmin) or np.any(params > pmax):
            pout = ""
            for pname, par, minp, maxp in zip(pnames, params, pmin, pmax):
                if par < minp:
                    pout += f"\n{pname[:11]:11s}  {minp: 12.5e} < {par: 12.5e}"
                if par > maxp:
                    pout += f"\n{pname[:11]:26s}  {par: 12.5e} > {maxp: 12.5e}"

            log.error(
                "Some initial-guess values are out of bounds:\n"
                "Param name           pmin          value           pmax\n"
                "-----------  ------------   ------------   ------------"
                f"{pout}"
            )

        nfree = int(np.sum(pstep > 0))
        ifree = np.where(pstep > 0)[0]  # Free parameter indices
        ishare = np.where(pstep < 0)[0]  # Shared parameter indices

        # Check output dimension:
        model0 = func(params, *indparams)
        if np.shape(model0) != np.shape(data):
            log.error(
                f"The size of the data array ({np.size(data)}) does not "
                f"match the size of the func() output ({np.size(model0)})"
            )


        # Check that output path exists:
        if savefile is not None:
            fpath, fname = os.path.split(os.path.realpath(savefile))
            if not os.path.exists(fpath):
                log.warning(
                    f"Output folder path: '{fpath}' does not exist. "
                    "Creating new folder."
                )
                os.makedirs(fpath)

        # At the moment, skip optimization when these dynesty inputs exist:
        if sampler == 'dynesty' \
                and ('loglikelihood' in kwargs or 'prior_transform' in kwargs):
            leastsq = None

        # Least-squares minimization:
        chisq_factor = 1.0
        if leastsq is not None:
            fit_output = fit(
                data, uncert, func, np.copy(params), indparams,
                pstep, pmin, pmax, prior, priorlow, priorup, leastsq)
            fit_bestp = fit_output['bestp']
            log.msg(
                f"Least-squares best-fitting parameters:\n  {fit_bestp}\n\n",
                si=2)

            # Scale data-uncertainties such that reduced chisq = 1:
            if chisqscale:
                chisq_factor = np.sqrt(fit_output['best_chisq']/(ndata-nfree))
                uncert *= chisq_factor

                # Re-calculate best-fitting parameters with new uncertainties:
                fit_output = fit(
                    data, uncert, func, np.copy(params), indparams,
                    pstep, pmin, pmax, prior, priorlow, priorup, leastsq)
                log.msg(
                    "Least-squares best-fitting parameters (rescaled chisq):"
                    f"\n  {fit_output['bestp']}\n\n",
                    si=2)
            params = np.copy(fit_output['bestp'])
        else:
            fit_output = None


        if resume:
            with np.load(savefile) as oldrun:
                uncert *= float(oldrun['chisq_factor'])/chisq_factor
                chisq_factor = float(oldrun['chisq_factor'])

        # Here's where the magic happens:
        if sampler in ['mrw', 'demc', 'snooker']:
            output = mcmc(
                data, uncert, func, params, indparams, pmin, pmax, pstep,
                prior, priorlow, priorup, nchains, ncpu, nsamples, sampler,
                wlike, fit_output, grtest, grbreak, grnmin, burnin, thinning,
                fgamma, fepsilon, hsize, kickoff, savefile, resume, log,
                pnames, texnames,
            )
        elif sampler == 'dynesty':
            output = nested_sampling(
                data, uncert, func, params, indparams,
                pmin, pmax, pstep, prior, priorlow, priorup, ncpu,
                thinning, resume, log, **kwargs,
            )


        # Get some stats:
        output['pnames'] = pnames
        output['texnames'] = texnames
        output['chisq_factor'] = chisq_factor

        if leastsq is not None:
            delta_log_post = output['best_log_post'] - fit_output['best_log_post']
            delta_pars = output['bestp'] - fit_output['bestp']
            if delta_log_post > 5.0e-8 and np.any(delta_pars != 0.0):
                log.warning(
                    "MCMC found a better fit than the minimizer:\n"
                    "MCMC best-fitting parameters:        (chisq={:.8g})\n{}\n"
                    "Minimizer best-fitting parameters:   (chisq={:.8g})\n{}".
                    format(
                        -2*output['best_log_post'], output['bestp'],
                        -2*fit_output['best_log_post'], fit_output['bestp']))

        # And remove burn-in samples:
        posterior, zchain, zmask = mu.burn(
            Z=output['posterior'], zchain=output['zchain'], burnin=output['burnin'])

        # TBD: make this user-configurable
        theme = mp.THEMES['blue']
        post = mp.Posterior(posterior, pnames=texnames[ifree], theme=theme)

        # Parameter statistics:
        bestp = output['bestp']
        sample_stats = ms.calc_sample_statistics(
            post.posterior, bestp, pstep, hpd=True,
        )
        stdp = output['stdp'] = sample_stats[3]
        median = sample_stats[0]
        med_low_bounds = sample_stats[4]
        med_high_bounds = sample_stats[5]


        log.msg(
            "\nParameter name     best fit   median      1sigma_low   1sigma_hi        S/N"
            "\n--------------- -----------  -----------------------------------  ---------",
            width=80)
        for i in range(nparams):
            pname = f'{pnames[i][0:15]:<15}'
            lo = med_low_bounds[i] - median[i]
            hi = med_high_bounds[i] - median[i]
            if i in ifree:
                snr = f"{np.abs(bestp[i])/stdp[i]:.1f}"
            elif i in ishare:
                idx = -int(pstep[i])
                snr = f"[share{idx:02d}]"
            else:
                snr = "[fixed]"
                lo = hi = 0.0
            log.msg(
                f"{pname} {bestp[i]:11.4e}  {median[i]:11.4e} "
                f"{lo:11.4e} {hi:11.4e}  {snr:>9s}",
                width=160,
            )

        # Fit statistics:
        best_chisq = output['best_chisq']
        log_post = -2.0*output['best_log_post']
        bic = output['BIC']
        red_chisq = output['red_chisq']
        std_dev = output['stddev_residuals']

        chisqscale_txt = f"sqrt(reduced chi-squared) factor: {chisq_factor:.4f}\n"
        if not chisqscale:
            chisqscale_txt = ''


        fmt = len(f"{bic:.4f}")  # Length of string formatting
        log.msg(
            f"\n{chisqscale_txt}"
            f"Best-parameter's chi-squared:       {best_chisq:{fmt}.4f}\n"
            f"Best-parameter's -2*log(posterior): {log_post:{fmt}.4f}\n"
            f"Bayesian Information Criterion:     {bic:{fmt}.4f}\n"
            f"Reduced chi-squared:                {red_chisq:{fmt}.4f}\n"
            f"Standard deviation of residuals:  {std_dev:.6g}\n",
            indent=2,
        )

        if savefile is not None or plots or closelog:
            log.msg("\nOutput sampler files:")

        # Save results (pop unpickables before saving, then put back):
        if savefile is not None:
            unpickables = ['dynesty_sampler']
            unpickables = np.intersect1d(unpickables, list(output.keys()))
            tmp_outputs = {key: output.pop(key) for key in unpickables}
            np.savez(savefile, **output)
            output.update(tmp_outputs)
            log.msg(f"'{savefile}'", indent=2)


        if plots:
            # Extract filename from savefile or default to sampler:
            fname = sampler if savefile is None else os.path.splitext(savefile)[0]
            # Include bestp in posterior plots:
            best_freepars = output['bestp'][ifree] if showbp else None

            bestp = best_freepars
            # Trace plot:
            savefile = f'{fname}_trace.png'
            mp.trace(
                output['posterior'], zchain=output['zchain'],
                burnin=output['burnin'], pnames=texnames[ifree],
                savefile=savefile, color=theme.color,
            )
            log.msg(savefile, indent=2)
            # Pairwise posteriors:
            savefile = f'{fname}_pairwise_posterior.png'
            post.plot(savefile=savefile)
            log.msg(savefile, indent=2)
            # Histograms:
            savefile = f'{fname}_marginal_posterior.png'
            post.plot_histogram(savefile=savefile)
            log.msg(savefile, indent=2)
            # RMS vs bin size:
            if rms:
                savefile = f'{fname}_RMS.png'
                residuals = output['best_model'] - data
                data_rms, rms_lo, rms_hi, stderr, binsize = ms.time_avg(residuals)
                mp.rms(
                    binsize, data_rms, stderr, rms_lo, rms_hi,
                    binstep=len(binsize)//500+1,
                    savefile=savefile,
                )
                log.msg(savefile, indent=2)
            # Guessing that indparams[0] is the X array for data as in y=y(x):
            if (indparams != []
                    and isinstance(indparams[0], (list, tuple, np.ndarray))
                    and np.size(indparams[0]) == ndata):
                try:
                    mp.modelfit(
                        data, uncert, indparams[0], output['best_model'],
                        savefile=fname+"_model.png")
                    log.msg(f"'{fname}_model.png'", indent=2)
                except:
                    pass

        # Close the log file if necessary:
        if closelog:
            log.msg(f"'{log.logname}'", indent=2)
            log.close()

        return output


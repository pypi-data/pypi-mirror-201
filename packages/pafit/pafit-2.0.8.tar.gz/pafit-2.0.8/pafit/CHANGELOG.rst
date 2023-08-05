Changelog
=========

V2.0.8: MC, Oxford, 3 April 2023
    - Included ``kwargs`` keyword passed to ``plot_velfield``.
    - Subtract ``np.median(vel)`` in the example.
    - Formatted documentation as docstring.
    - Published documentation on PyPi.

V2.0.7: MC, Oxford, 23 March 2021
    - Some documentation updates.

V2.0.6: MC, Oxford 12 May 2018
    - Dropped Python 2.7 support.

V2.0.5: MC, Oxford, 17 April 2018
    - Changed imports for plotbin as package.

V2.0.4: MC, Oxford, 17 March 2017
    - Use Numpy ``np.percentile`` instead of deprecated Scipy version.

V2.0.3: MC, Oxford, 7 September 2015
    - Changed color of plotted lines.
    - Check matching of input sizes.

V2.0.2: MC, Sydney, 2 February 2015
    - Fixed possible program stop.

V2.0.1: MC, Oxford, 25 May 2014
    - Support both legacy Python 2.7 and Python 3.

V2.0.0: MC, Oxford, 10 April 2014
    - Translated from IDL into Python.

V1.3.1: MC, Oxford, 2 December 2013
    - Uses CAP_RANGE routine to avoid potential naming conflicts.
    - Uses TOLERANCE keyword of TRIANGULATE to try to avoid IDL error
      "TRIANGULATE: Points are co-linear, no solution."

V1.3.0: MC, Oxford, 8 October 2013
    - The program is two orders of magnitude faster, thanks to a
      new ``cap_symmetrize_velfield`` routine.

V1.2.0: MC, Oxford, 23 March 2010
    - Includes error in chi^2 in the determination of angErr.
      Thanks to Davor Krajnovic for reporting problems.

V1.1.5: MC, Oxford, 14 October 2009
    - Overplot best PA on data. Some changes to the documentation.

V1.1.4: MC, Oxford, 31 March 2009
    - Clarified that systemic velocity has to be subtracted from VEL.
   
V1.1.3: MC, Leiden, 25 May 2008
    - Determine plotting ranges from velSym instead of vel.
      Thanks to Anne-Marie Weijmans.

V1.1.2: MC, Oxford, 19 October 2007
    - Force error to be larger than 1/2 of the angular step size.
   
V1.1.1: MC, Oxford, 17 October 2007
    - Corrected handling of NSTEPS keyword. Thanks to Roland Jesseit.
   
V1.1.0: MC, Oxford, 9 October 2007
    - Written documentation.

V1.0.0: Michele Cappellari, Leiden, 30 May 2005
    - Written and tested

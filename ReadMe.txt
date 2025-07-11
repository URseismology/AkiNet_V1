AkiNet ReadMe
Siyu Xue
July 11, 2025

*************** Environment ***************
Python 3.12.8 was used for this project. We also provide the "environment.yml" for your reference. 


*************** Code ***************

*** {1} PINN_inverse_PV.ipynb ***
1. Plot Fig. 2
2. Plot Fig. 3
(3). Plot S2

*** {2} FindPeakEnve.ipynb ***
1. Plot Fig. S1
2. Generate the Bessel Envelope files: "BesselEnveRay.csv" and "BesselEnveLove.csv"

*** {3} BoxRegionTest.ipynb ***
1. Plot Fig. 4
2. Can plot the AkiEstimate vs AkiNet for each individual station pair (not included in the paper)

*** {4} PINN_Hessian.ipynb ***
1. Plot Fig. S4
2. Plot Fig. S5

Note: 
(1) the map in Fig. S3 is taken from ADAMA2 paper. The small plot showing the station locations and station connections can be easily plotted from 'Boxconn.csv'
(2) please update your local data directory in section [0] before running any of the notebooks 
(3) if need to use AkiNet for other inversion tasks, follow the examples in "PINN_inverse_PV.ipynb". AkiNet as well as other necessary functions are defined in sections [1] to [4] in the notebook


*************** PINNData ***************

{1} AkiEst: AkiEstimate results used in 'PINN_inverse_PV.ipynb' and 'FindPeakEnve.ipynb'
{2} NCF: NCF data used in 'PINN_inverse_PV.ipynb' and 'FindPeakEnve.ipynb'
{3} BoxRegion: NCF data and AkiEstimate results at the selected box region. 'Boxconn.csv' contains the list of station connections within the selected box region 
{4} "BesselEnveRay.csv" and "BesselEnveLove.csv": Bessel peak envelopes for normalizing the observed NCF; used in all notebooks. 
{5} "SDISPR.ASC" and "SDISPL.ASC": Rayleigh and Love wave phase velocities for AK135 model 

Note:
(1) all AkiEstimate and NCF data are taken from the previously published dataset: A Short©\Period Surface©\Wave Dispersion Dataset for Model Assessment of Africa¡¯s Crust: ADAMA by Tolulope Olugboji and Siyu Xue. 



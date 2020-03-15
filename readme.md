## CAPP 30122: Final Project - Chicago Public Schools SQRP Playground
### Ali Pelczar, Lily Grier, and Launa Greer
 
#### Processes a school quality rating policy (SQRP) for the Chicago Public Schools (CPS) by assigning rating and attainment scores for each high school in the district and then generating a bias score for the SQRP as a whole.

![alt text](sqrp/static/img/Configure_Model.JPG "Configure Model")

![alt text](sqrp/static/img/View_Results.JPG "View Results")

![alt text](sqrp/static/img/View_Bias_Score.JPG "View Bias Score")


Using a Django web interface, the user selects relative weights for each school 
indicator using slider widgets. If the user does not want to include an input in
the rating system, the user should leave that input’s weight as zero. The 
backend program then takes those inputs, generates a rating system based on those
inputs, and assigns each school a rating accordingly. If inputs are missing for
a particular school, the algorithm reassigns those weights to a different inputs
(for details about this reassignment, see the “Reassignment Logic” section of
the Appendix). The software then calculates a bias score for each rating system
the user specifies, which communicates how well schools’ scores align with the 
demographics of their student body. The interface returns the bias score for 
the specified policy along with individual ratings for each of the schools 
based on the policy.
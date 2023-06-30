<h1 align='center'>
<br>
<img src="https://180dc.org/wp-content/uploads/2022/04/ibm-logo-.png" alt="IBM Course" width="200">
<br>
 IBM Data Science Capstone
 
 ## Project Scenario
 
SpaceX is a leading company in the space industry, known for making space travel affordable. Its achievements include sending spacecraft to the International Space Station, launching a satellite constellation that provides internet access, and sending manned missions to space. The company's innovative reuse of the first stage of its Falcon 9 rocket has contributed to the relatively low cost of its launches, which are priced at $62 million per launch. In comparison, other providers that are unable to reuse the first stage cost upwards of $165 million each. By determining if the first stage will land, the price of the launch can be estimated.

In this capstone project, you will play the role of a data scientist working for a new rocket company, Space Y, founded by billionaire industrialist Allon Musk, that aims to compete with SpaceX. Your task is to determine the price of each launch by gathering information about SpaceX and creating dashboards for your team. Additionally, you will predict whether SpaceX will reuse the first stage by training a machine learning model using public information, instead of relying on rocket science to determine the success of the landing.

To achieve this, public data and machine learning models will be utilized to predict whether SpaceX or a competing company can reuse the first stage.

## Requirements

To run the code in this project, you will need the following libraries installed:

`pip install pandas numpy matplotlib seaborn dash folium scikit-learn requests sqlalchemy wget beautifulsoup4`

## Data Collection

To gather data for the project, the following steps were taken:

### API

1. Requested data on rocket launches from the SpaceX API.
2. Decoded the response using .json() and converted it to a dataframe using
   .json_normalize().
3. Requested information about the launches from SpaceX API using custom functions.
4. Created a dictionary from the data.
5. Converted the dictionary to a dataframe.
6. Filtered the dataframe to include only Falcon 9 launches.
7. Replaced missing values of Payload Mass with the calculated .mean().
8. Exported the data to a CSV file.

### Web Scraping

1. Requested Falcon 9 launch data from Wikipedia.
2. Created a BeautifulSoup object from the HTML response.
3. Extracted column names from the HTML table header.
4. Collected data by parsing HTML tables.
5. Created a dictionary from the data.
6. Converted the dictionary to a dataframe.
7. Exported the data to a CSV file.

## Data Wrangling

To prepare the data for analysis, the following steps were taken:

- Converted outcomes into 1 for successful landings and 0 for unsuccessful landings.

## Exploratory Data Analysis (EDA)

#### EDA with Visualization

Visualizations were created to analyze relationships and show comparisons.

#### EDA with SQL

The data was queried to gain a deeper understanding of the data.

#### Maps with Folium

Maps were created using Folium to visualize launch sites, view launch outcomes, and see distances to proximities.

## Predictive Analysis

To predict whether SpaceX will reuse the first stage, the following steps were taken:

1. Created a NumPy array from the Class column.
2. Standardized the data with StandardScaler by fitting and transforming the data.
3. Split the data using train_test_split.
4. Created a GridSearchCV object with cv=10 for parameter optimization.
5. Applied GridSearchCV on different algorithms, including Logistic Regression, Support 6
6. Vector Machine, Decision Tree, and K-Nearest Neighbor.
7. Calculated the accuracy on the test data using .score() for all models.
8. Assessed the confusion matrix for all models.
9. Identified the best model using F1_Score and Accuracy.

## Presentation

The findings from the project were presented in a pdf presentation that showcases the insights and trends identified from the data.

## Conclusion

The models performed similarly on the test set, with the decision tree model slightly outperforming on training. Launch success increases over time, and all launch sites are located close to the coast. Among all launch sites, KSC LC-39A has the highest success rate, with a 100% success rate for launches less than 5,500 kg. ES-L1, GEO, HEO, and SSO have a 100% success rate for orbits, and across all launch sites, the success rate increases with the payload mass.

### Additional Things to Consider

To build on the predictive analytics results and understand if the findings can be generalized to a larger dataset, a larger dataset should be considered. Additional feature analysis or principal component analysis should be conducted to see if it can improve accuracy. XGBoost, a powerful model not utilized in this study, could also be explored to see if it outperforms other classification models.

## Acknowledgements

I would like to thank IBM and Coursera for providing this opportunity to learn and practice data science. The project was challenging, but also rewarding, and it has helped me develop skills in data collection, data wrangling, statistical analysis, predictive analysis, dashboard creation, and presentation.

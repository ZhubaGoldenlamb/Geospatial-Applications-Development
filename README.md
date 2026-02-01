## Interactive Dashboards & Web GIS Applications
**Power BI • ArcGIS Experience Builder • Custom Web Mapping**

This section documents applied geospatial projects focused on **interactive analysis, data-driven decision support, and cartographic design**. Projects range from full dashboard applications to independent web mapping and basemap development work.

---

### 📊 Project 1: Interactive Restaurant Analysis Dashboard  
**Power BI · ArcGIS Experience Builder · Survey123**

🔗 **Live Applications**  
- **Power BI Dashboard:** [View Interactive Dashboard](https://app.powerbi.com/groups/me/reports/dfd5324f-eff7-4a38-ac2f-d07c83833f84/9b943d3431319454036d?experience=power-bi)  
- **Web GIS Application (Experience Builder):** [Open Web App](https://csulb.maps.arcgis.com/home/item.html?id=f1858b7291a74810b991c77a5711407f)
- **Survey123 Form:** [Submit / View Survey](https://csulb.maps.arcgis.com/home/item.html?id=e67d65f4376440c0b955b1871b9a5dfd)

**Overview**  
This project integrates Yelp restaurant review data with user-submitted Survey123 responses to support comparative spatial and qualitative analysis. The system consists of a Power BI dashboard, an ArcGIS Experience Builder web application, and a Survey123 form. Power BI serves as the primary analytical interface, while Experience Builder extends spatial exploration beyond the constraints of a dashboard layout.

#### **Application Components**

**Power BI Dashboard (Primary Analysis Interface)**  
<img src="/screenshots/PowerBI_Dashboard.PNG" width="1500">

**ArcGIS Experience Builder Web App (Extended Spatial Exploration)**  
<img src="/screenshots/Online_Web_App.PNG" width="1500">

**Survey123 Form (User Data Collection)**  
<img src="/screenshots/Survey.PNG" width="550">

#### **Map Implementation: ArcGIS Map for Power BI**
The dashboard uses **ArcGIS Map for Power BI** rather than Azure Maps. Azure Maps was evaluated but did not provide the level of reliability and GIS-specific functionality required for this project. ArcGIS Map for Power BI allowed for better handling of point data, attribute-driven symbology, and pop-up behavior, while maintaining consistency with ArcGIS Online–hosted layers used elsewhere in the workflow.

#### **Role of ArcGIS Experience Builder**
Power BI is optimized for structured comparison and filtering, but is limited in terms of free-form spatial interaction. To address this, an ArcGIS Experience Builder web application is linked directly from the Power BI dashboard. This allows users to transition from summary analytics to deeper spatial exploration, providing greater flexibility for interacting with restaurant locations, ratings, and survey feedback.

#### **Key Design Decisions**
- The dashboard is intentionally divided into two vertical sections:
  - **Top section:** Aggregated Yelp-based metrics (map, charts, summary cards)
  - **Bottom section:** Survey submissions and survey-derived summaries
- Survey data is kept distinct from aggregated Yelp statistics to avoid conflation while still supporting comparison.
- The Experience Builder application links Yelp and survey data through a shared restaurant name identifier, enabling map pop-ups to display both qualitative survey feedback and aggregated Yelp review information.

#### **Core Features**
- Interactive map displaying restaurant locations  
- Bar charts summarizing average Yelp ratings by restaurant  
- Summary cards showing counts and overall averages  
- Survey response table with user-submitted ratings and comments  
- Dropdown slicer for filtering Yelp reviews by rating class  
- Linked web mapping application for extended spatial interaction  

#### **Rating Class Dropdown (DAX Implementation)**
To support categorical filtering of continuous Yelp ratings, a calculated **Rating Class** field was created and applied as a dropdown slicer. Selecting a rating class dynamically filters the map, bar charts, and summary cards simultaneously.

```DAX
RatingClass =
SWITCH(
    TRUE(),
    [YelpRating] >= 4.7, "4.7+",
    [YelpRating] >= 4.5, "4.5 – 4.69",
    [YelpRating] >= 4.4, "4.4 – 4.49",
    [YelpRating] >= 4.0, "4.0 – 4.39",
    "Below 4.0"
)
```
#### **Technical Highlights**
- ArcGIS Map for Power BI used in place of Azure Maps for greater GIS functionality  
- Consistent color usage across visuals to reinforce meaning  
- Bold axis labels and external bar values for readability  
- Cleaned and validated Excel source data to ensure reliable pop-ups and hyperlinks  
- Standardized field names across Power BI and ArcGIS Online for seamless integration  
- Experience Builder widgets configured to maintain usability across different screen sizes  

#### **Tools**
- Power BI Desktop  
- ArcGIS Online  
- ArcGIS Experience Builder  
- ArcGIS Survey123  
- Excel (data cleaning and validation)

---

## Cartography & Web Mapping Projects

This section highlights independent geospatial mapping projects focused on **cartographic design, visual hierarchy, and spatial storytelling**, distinct from application or dashboard development.

---

### 🗺️ Olympic Venues & Transportation Flow  
**Custom ArcGIS Vector Basemap Design**

🔗 **Interactive Web Map:** https://arcg.is/1LrKa80

**Summary**  
This project demonstrates custom vector basemap design using **ArcGIS Online’s Vector Tile Style Editor**, with an emphasis on reducing visual noise while enhancing thematic clarity. The basemap was intentionally designed to support Olympic venue data without overpowering it.

**Design Highlights**
- Light and dark blue used for **water features and major highways** to establish circulation patterns
- Reduced font sizes and road widths to maintain a subdued background hierarchy
- Yellow label halos added to improve place-name legibility
- Dark green parks spaced and softened to act as visual accents rather than dominant features
- Olympic venue points styled in **red**, completing a balanced Olympic color palette (red, green, blue, black, white)
- Blue polygons used to reinforce venue visibility across scales
- Highway styling emphasizes how transportation corridors feed into venue locations

**Tools**
- ArcGIS Online  
- ArcGIS Vector Tile Style Editor  

**Focus**
Cartographic design, vector basemap styling, visual hierarchy, and thematic support mapping.

---


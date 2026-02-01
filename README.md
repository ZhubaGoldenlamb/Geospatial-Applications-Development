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
<img src="/screenshots/Online_Web_App.png" width="1500">

**Survey123 Form (User Data Collection)**  
<img src="/screenshots/Survey.PNG" width="550">

#### **Role of ArcGIS Experience Builder**
The ArcGIS Experience Builder application provides deeper spatial interaction beyond the Power BI dashboard. Each restaurant point includes a structured pop-up that integrates both **user-submitted survey responses** and **aggregated Yelp review data**.

Within the pop-up:
- The **“Experience”** and **“Write a Review”** sections display Survey123 responses, allowing users to view qualitative feedback and contribute new survey entries.
- Below the survey content, **Yelp review data** is presented, including aggregated ratings and review metrics derived from online sources.

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

### 🗺️ Project 2: Olympic Venues & Transportation Flow  
**Custom ArcGIS Vector Basemap Design**

🔗 **Map Viewer:** [Open in Map Viewer](https://www.arcgis.com/apps/mapviewer/index.html?webmap=a84a149775b0419e90808eceb19bc8c5)

**Overview**  
This project focuses on custom **vector basemap design** using ArcGIS Online’s **Vector Tile Style Editor**. The goal was to create a basemap that supports thematic Olympic venue data while maintaining visual restraint, clear hierarchy, and legibility across scales. Rather than relying on a default basemap, the styling was intentionally modified to reduce visual noise and emphasize transportation connectivity.

<img src="/screenshots/olympic_basemap.png" width="900">

#### **Cartographic Design Strategy**
- Light and dark blue tones were applied to **water features and major highways** to establish visual continuity and highlight circulation patterns.
- Road widths and label font sizes were reduced to prevent the basemap from overpowering thematic layers.
- Yellow halos were added around place names to improve label legibility against varied backgrounds.
- Parks were symbolized in dark green and spatially softened to act as accents rather than dominant visual elements.

#### **Thematic Layer Design**
- Olympic venue locations are symbolized in **red**, immediately distinguishing them from the basemap.
- Red venue points complete a balanced Olympic-inspired color palette consisting of **red, green, blue, black, and white**.
- Blue polygons were added around venues to reinforce visibility and contrast across multiple zoom levels.
- Highway styling emphasizes how regional transportation corridors feed into venue locations, supporting spatial interpretation of accessibility.

#### **Design Intent**
The basemap was designed to function as a supporting structure rather than a focal element. Color, symbol weight, and spacing were deliberately restrained so that Olympic venues and transportation relationships remain visually prominent without distraction from underlying geographic context.

#### **Tools**
- ArcGIS Online  
- ArcGIS Vector Tile Style Editor  

#### **Focus**
Cartographic design, vector basemap styling, visual hierarchy, and thematic support mapping.

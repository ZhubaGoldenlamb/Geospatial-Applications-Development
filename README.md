# Interactive Dashboards & Web GIS Applications  
**Power BI • ArcGIS Experience Builder • Survey123**

This repository documents an applied application-development project integrating **Power BI dashboards**, **ArcGIS Experience Builder Web GIS**, and **Survey123 data collection**. The project demonstrates how multiple platforms can be connected to support interactive exploration, user input, and feature-level context within geospatial applications.

---

## Live Applications

- **ArcGIS Experience Builder Web App:**
  [View interactive Web App](https://experience.arcgis.com/experience/f1858b7291a74810b991c77a5711407f)

- **Survey123 Form:**  
  [View Survey Form](https://survey123.arcgis.com/share/e67d65f4376440c0b955b1871b9a5dfd?portalUrl=https://csulb.maps.arcgis.com)

- **Power BI Dashboard (PDF export):**  
 [View Comprehensive PowerBI Dashboard](https://app.powerbi.com/view?r=eyJrIjoiMzY4NzdmMDMtNDllNy00ZDkwLThiYTEtMjY0MTYzMjE5ODFjIiwidCI6ImQxNzU2NzliLWFjZDMtNDY0NC1iZTgyLWFmMDQxOTgyOTc3YSIsImMiOjZ9&embedImagePlaceholder=true)

---

## Project Overview

The application compares **aggregated Yelp restaurant reviews** with **user-submitted survey responses** collected via Survey123. Rather than blending survey data into summary statistics, survey responses are in seperated. In the **PowerBI Dashboard**, interface is intentionally divided into two sections:
- **Top section:** Yelp-based metrics (map, charts, cards)
- **Bottom section:** Survey submissions and survey-derived summaries. This separation prevents dilution of either dataset while still allowing meaningful comparison.
The larger **Web App** version integrates Yelp data and survey responses through a shared restaurant name identifier, so when you click on the point in the map, the **map pop-ups** have both qualitative feedback and aggrigated yelp review information. 

---

## Power BI Dashboard Design

The Power BI dashboard integrates Yelp data with the top layer of visual compenets, and the survey data is integrated with their respective visual components.

### Visual components
- Interactive map showing restaurant locations
- Bar charts summarizing average Yelp ratings by restaurant
- Cards displaying counts and overall averages
- Survey response table showing submitted ratings and comments

### Design choices
- Bold axis labels for readability
- Bar values positioned outside bars for clarity
- Consistent color scheme across charts
- Uniform sizing of dashboard elements
- Header color `#EDEDED` and value color `#F5F5F5` to match the background

Charts representing similar data use the same color to reinforce meaning.

---

## Rating Class Dropdown (Implementation)

To allow filtering of Yelp reviews by rating level, I created a **Rating Class** field that categorizes continuous Yelp ratings into discrete groups.

### Example DAX (conceptual)
```dax
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
---
The **Rating Class** field is used in a dropdown slicer. Selecting a rating class automatically filters:
- The map
- The bar chart
- Summary cards

This allows users to focus on higher-rated restaurants (for example, 4.5+ stars) without manually filtering individual visuals.

---

## Map Interactivity & Tooltips

Restaurant points on the map are symbolized by color based on rating class. Hovering over a point displays:
- Restaurant name and address
- Average Yelp rating
- Rating keywords
- Cuisine type and price range

Each restaurant is color-coded to match the legend, allowing users to quickly interpret spatial patterns in ratings.

---

## Survey Data Cleaning & Link Validation

Before importing Yelp Collected data into Power BI and ArcGIS Online, the Excel was cleaned to ensure pop-ups and links functioned correctly. This was especially important for the map pop ups in the PowerBI Dashboard and the Web App.

This process included:
- Removing extraneous text and whitespace from hyperlink cells
- Ensuring each hyperlink cell contained only a valid URL
- Verifying that the **“View”** action in pop-ups worked reliably
- Standardizing field names across Power BI and ArcGIS Online

Clean, predictable field values were necessary for both Power BI and Experience Builder, which rely on consistent data structures for interactive elements.

---

## ArcGIS Experience Builder Implementation

The Experience Builder application includes:
- A map widget displaying restaurant locations
- A list widget showing restaurant names and ratings
- Chart widgets summarizing rating distributions
- Filter buttons for restaurant selection

Widget placement and sizing were configured to:
- Prevent overlap with map features
- Allow scrolling within the restaurant list
- Accommodate legends, charts, and interactive controls
- Maintain usability across different screen sizes

Because Experience Builder applications are data-driven rather than static layouts, careful configuration and testing were required prior to publishing.

---

## Tools & Platforms

- Power BI Desktop
- ArcGIS Online
- ArcGIS Experience Builder
- ArcGIS Survey123
- Excel (data cleaning and validation)

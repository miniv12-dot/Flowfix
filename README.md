# 💧 FlowFix

> **Smart Municipal Water Infrastructure Tracking Platform** > A full-stack civic tech application bridging the spatial communication gap between citizens and municipal engineering divisions. Log leak locations via predictive address lookups, track automated workflows, and review real-time regional analytical data.

---

## 🚀 Key Technical Features

* **Google-Like Predictive Address Autocomplete:** Integrated `Leaflet GeoSearch` to fetch real-time address predictions from OpenStreetMap APIs as the user types.
* **Geospatial Coordinate Capture:** Automatically translates address selection or manual click-to-pin mapping into precise latitude and longitude metadata.
* **Real-Time Data Visualizations:** Implemented `Chart.js` with the `DataLabels` plugin to render dynamic severity doughnuts and operational status bar charts.
* **Persistent Theme Engine:** Responsive dark and light mode UI architecture using Bootstrap 5.3 built-in variables and synchronized with browser cache state via `localStorage`.

---

## 🛠️ Built With

* **Backend:** Python, Django
* **Database:** PostgreSQL
* **Frontend UI:** HTML5, CSS3, Bootstrap 5.3 (Glassmorphic design utilities)
* **Mapping API:** Leaflet.js, Leaflet GeoSearch (OSM Provider)
* **Analytics Layer:** Chart.js, ChartJS-Plugin-DataLabels

---

## 📊 Database Architecture

The core data structures utilize rigid field validation and relational integrity keys.

### Entity Relationship Abstract

| Model | Field Name | Data Type | Constraints / Purpose |
| :--- | :--- | :--- | :--- |
| **FaultReport** | `id` | AutoField | Primary Key |
| | `title` | CharField | max_length=200 |
| | `description` | TextField | Detailed fault context |
| | `latitude` | DecimalField | max_digits=9, decimal_places=6 |
| | `longitude` | DecimalField | max_digits=9, decimal_places=6 |
| | `street_address` | CharField | Optional nearest landmark metadata |
| | `severity` | CharField | Choices: Low, Medium, High |
| | `evidence_image` | ImageField | Local storage binary path upload |
| **WorkOrder** | `id` | AutoField | Primary Key |
| | `report` | ForeignKey | Relates 1-to-1 with `FaultReport` (CASCADE) |
| | `status` | CharField | Choices: PENDING, DISPATCHED, IN_PROGRESS, RESOLVED |
| | `assigned_team` | CharField | String lookup for deployed technical crew |
| | `date_updated` | DateTimeField | auto_now=True |

---

## 💻 Local Ingestion & Deployment

### Prerequisite Environment Settings
Ensure Python 3.10+ and a PostgreSQL server instance are running locally.

```bash
# Clone the repository
git clone [https://github.com/YOUR_USERNAME/FlowFix.git](https://github.com/YOUR_USERNAME/FlowFix.git)
cd FlowFix

# Set up and activate local virtual environment space
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install third-party Python modules
pip install django psycopg2-binary pillow

# Apply schema modifications into relational database target
python manage.py makemigrations
python manage.py migrate

# Initialize administrative root user credentials
python manage.py createsuperuser

# Launch local deployment host
python manage.py runserver
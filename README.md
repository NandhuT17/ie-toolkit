# Time Study System

A web-based **Time Study Management System** built with **Django** to simplify industrial time studies. The application enables administrators to manage operators and machines, perform time studies using QR code-based operator identification, calculate production capacity, and export reports to Excel.

---

## Features

### Operator Management
- Add and manage operators
- Automatic QR code generation
- Download generated QR codes

### Machine Management
- Add machine models
- Prevent duplicate machine entries

### Time Study
- QR code scanning to identify operators
- Built-in stopwatch for recording cycle times
- Automatic average cycle time calculation
- Automatic production capacity calculation
- Batch-wise operation recording

### Excel Export
Export reports containing:
- Date
- Operator details
- Machine
- Batch
- Operation
- Five readings
- Average time
- Allowance
- Capacity
- Target
- Difference
- Efficiency (%)

## Project Structure

```
toolkit/
│
├── base/
│   ├── migrations/
│   ├── templates/
│   ├── static/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── admin.py
│
├── toolkit/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── media/
├── static/
├── requirements.txt
├── manage.py
└── build.sh
```

---

## Installation

### Clone the repository

```bash
git clone https://github.com/NandhuT17/ie-toolkit.git
cd ie-toolkit
```

### Create a virtual environment

Windows

```bash
python -m venv venv
venv\Scripts\activate
```


### Install dependencies

```bash
pip install -r requirements.txt
```

### Apply migrations

```bash
python manage.py migrate
```

### Run the development server

```bash
python manage.py runserver
```

Open

```
http://127.0.0.1:8000/
```

---


## Capacity Calculation

Average Cycle Time

```
Average = (Reading1 + Reading2 + Reading3 + Reading4 + Reading5) / 5
```

Production Capacity

```
Capacity = 3600 / Average
```

Efficiency (Excel Report)

```
Efficiency (%) = (Capacity / Target) × 100
```

---


## Contributor

**Sanjeev** - JavaScript

## Author

**Nandhu**

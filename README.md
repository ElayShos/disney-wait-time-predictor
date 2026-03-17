# Disney Wait Time Predictor

This project predicts wait times for Walt Disney World's popular rides using historical data and a Machine Learning model.
It was built as a student project to practice data analysis and basic machine learning, and to help me plan future trips.

---

## Features

* Predicts wait times based on:

  * Ride name
  * Day of the week
  * Hour of the day
* Uses a Random Forest Model trained on past data

---

## Technologies

* Python
* pandas
* scikit-learn

---

## Setup

Clone the repository:

```bash
git clone https://github.com/ElayShos/disney-wait-time-predictor.git
cd disney-wait-time-predictor
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## How to run

Run the prediction script:

```bash
python predict.py
```

---

## Usage

After running `predict.py`, you will be prompted to enter:

Ride name
Examples:

* Space Mountain
* Pirates of the Caribbean
* Frozen Ever After
* Test Track
* Tower of Terror

Day of the week (0–6)

* 0 = Monday
* 1 = Tuesday
* 2 = Wednesday
* 3 = Thursday
* 4 = Friday
* 5 = Saturday
* 6 = Sunday

Hour of the day (0–23)

* 0 = 00:00
* 13 = 13:00
* 23 = 23:00

Make sure to select an hour in which the park is open - most parks are open from 9:00 to 21:00

---

## Example

Input:
Ride: tower of terror
Day: 5
Hour: 14

Output:
Result for THE TWILIGHT ZONE TOWER OF TERROR: 37.8m (+/- 7.9)

---

## Notes

* The predictions are based on historical data. Although predictions do not give real-time information, they are based upon a system that continuously pulls real-time data from the parks.
* Accuracy is set to improve as the system accumulates more and more data over time.
* As data from over the year, and over years keeps accumulating, new features can be added such as predicting which season/month is the best to go.

---

## Purpose

This project was created for 2 reasons:
1. As a learning opportunity for me to keep growing my coding and technical skills.
2. As a real helper to plan my trips to the Orlando parks, as a very big fan who visits frequently.

---

## Skills acquired during the development

* Learning a new API
* Working with real datasets
* Using pandas for data processing
* Training a machine learning model

---

# Race Simulation Dashboard

A Flask-based web application that simulates a race, including multiple cars with dynamic attributes such as lap time, tire life, and fuel levels. The web interface allows users to view race data, advance laps, and interact with the race via an API.

Temporary Development Link:

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Getting Started](#getting-started)
- [API Endpoints](#api-endpoints)
- [Running the Application](#running-the-application)
- [Testing](#testing)
- [Deployment](#deployment)
- [License](#license)

## Overview

This application simulates a car race with a dynamic dashboard that displays the race status. Users can interact with the race by advancing laps and viewing each car's performance metrics such as lap time, tire life, and fuel level.

The application includes:
- A Flask-based backend API that allows users to push and pull race data.
- A dynamic HTML front-end that fetches race data using JavaScript and displays it in real-time.

## Features

- **Race Simulation**: Advance through laps and track the performance of different cars.
- **API Integration**: Push and pull data through RESTful API endpoints.
- **Interactive Dashboard**: View race status and car performance metrics in real-time on the web interface.

## Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: HTML5, JavaScript (Fetch API)
- **Database**: (None - Using in-memory data structures for simulation)
- **Testing**: Pytest
- **CI/CD**: GitLab CI

## Getting Started

### Prerequisites

Docker to run the docker image

### Installation

1. Clone this repository:

   ```bash
   git clone https://gitlab.com/24fa-csci4830/group-1.git
   cd group-1

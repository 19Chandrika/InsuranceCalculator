# Insurance Premium Calculator

A full-stack web application that estimates insurance premiums for **Health, Vehicle, Life, and Travel Insurance** using predefined business rules. The application calculates the premium amount, 18% GST, total payable amount, and EMI options through a simple and responsive user interface.

## Features

* Health, Vehicle, Life, and Travel insurance support
* Dynamic input forms based on insurance type
* Premium calculation using predefined rules
* Automatic GST (18%) calculation
* Total payable amount calculation
* EMI options (3, 6, 9, and 12 months)
* RESTful API using Spring Boot
* Responsive frontend with HTML, CSS, and JavaScript

## Tech Stack

* Java 17
* Spring Boot
* REST API
* HTML5
* CSS3
* JavaScript
* Fetch API
* JSON

## Project Structure

```text
InsuranceCalculator/
├── src/
│   ├── main/
│   │   ├── java/
│   │   │   └── com/calculate/insurance/
│   │   ├── resources/
│   │   │   └── static/
│   │   │       └── index.html
│   └── test/
├── pom.xml
└── README.md
```

## Premium Calculation Rules

* **Health Insurance:** Coverage Amount × 2% + ₹1,000 per member (+₹2,000 if age > 45)
* **Vehicle Insurance:**

  * Car: Vehicle Value × 3%
  * Bike: Vehicle Value × 2%
  * * ₹500 × Vehicle Age
* **Life Insurance:** Coverage Amount × 1.5% + ₹300 × Policy Term (+₹1,500 if age > 40)
* **Travel Insurance:** Trip Cost × 1% + ₹50 × Travel Days + ₹300 × Number of Travellers
* **GST:** 18% of Premium
* **EMI:** Available for 3, 6, 9, and 12 months

## Getting Started

### Prerequisites

* Java 17+
* Maven 3.8+
* IDE (IntelliJ IDEA / Eclipse / VS Code)

### Run the Project

```bash
git clone https://github.com/your-username/InsuranceCalculator.git
cd InsuranceCalculator
mvn spring-boot:run
```

Open your browser and visit:

```text
http://localhost:8080
```

## API Endpoint

```http
POST /api/calculate-premium
```

Returns the premium amount, GST, total payable amount, and EMI options based on the submitted insurance details.


## Future Enhancements

* User authentication
* Database integration
* Policy comparison
* PDF report generation
* Email notifications
* Responsive mobile UI

## License

This project is developed for educational and academic purposes.

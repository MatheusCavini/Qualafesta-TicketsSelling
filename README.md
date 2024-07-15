# Qualafesta - Tickets Selling Platform

## Introduction
This project implements a complete online platform for event tickets e-commerce. It was entirely create using Django framework for Python language, together with a sqlite3 database.<br>
The platform supports 3 categories of users: 
- **Organizers**: those who can create events on the platform and tickets to be sold.
- **Customers**: those who can buy tickets for existing events through the platform.
- **Access Controllers**: event staff that can use the platform to verify tickets and admit customers on events.

The project was created as part of the discipline "Information Systems" (PMR3304) for my Mechatronics Engineering course at Escola Politécnica da Universidade de São Paulo (USP).

## Demonstration 
### Organizer 
[organizerVideo.webm](https://github.com/user-attachments/assets/5cac558f-acee-4ecc-aa7e-d828e40b4d7c)

### Customer 
[customerVideo.webm](https://github.com/user-attachments/assets/51a47e14-ec8f-4e09-80c8-29fb3019eddf)

### Access Controller 
[controllerVideo.webm](https://github.com/user-attachments/assets/0794cf9f-b401-472c-ac61-138ba1f2d093)

## Features
- Authorization logic, redirecting each categorie of user to its own specific pages through a single login page.
- **For organizers**: creating and modifying events and their attractions and tickets. Besides, monitoring how many tickets from each category have been sold.
- **For customers**: searching for events by name and description; visualizing all information about an event; buying tickets for an event; visualizing the QR Codes and identifiers for each bought ticket.
- **For access controllers**: scanning QR Codes of tickets from an especific event or typing its identifier in order to validate a customer entrance; receive a warning if a scanned ticket has already been used.

Note: payment logic is purely representative and there is no integration with real payment methods.
 

#!/bin/bash

curl -d '{"CustomerName": "Suke", "Contact": 9880112342, "Seats": ["a2", "a3"], "BusId": 2}' -H "Content-Type: application/json" -X POST http://localhost:5000/api/updateseat

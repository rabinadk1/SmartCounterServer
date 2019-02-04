#!/bin/bash

curl -d '{"Username":"maverick", "Password":"testing", "CounterId":1, "Contact":9844666021}' -H "Content-Type: application/json" -X POST http://localhost:5000/register

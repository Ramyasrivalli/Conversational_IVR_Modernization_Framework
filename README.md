# Conversational-IVR-Modernization-Framework
Modernization of legacy VXML-based IVR into a cloud-enabled conversational AI system using ACS and API-based integration while preserving backend infrastructure.
Modern IVR Integration – IRCTC Use Case

This project implements a conversational AI-powered IVR system that modernizes legacy IVR systems using FastAPI middleware and Twilio voice integration.

## Features
- PNR Status Check
- Train Schedule Query
- Ticket Booking Assistance
- Ticket Cancellation Assistance
- Voice interaction via Twilio
- Integration Layer connecting legacy IVR with backend services

## Architecture

User Call  
↓  
Twilio Voice Gateway  
↓  
FastAPI Integration Layer  
↓  
Intent Detection Engine  
↓  
Backend Service  
↓  
Response Formatter  
↓  
Voice Response

## Technologies Used
- Python
- FastAPI
- Twilio
- Ngrok
- GitHub

## Use Case
IRCTC Customer Support IVR System

Users can call the system and request:
- PNR Status
- Train Schedule
- Ticket Booking Info
- Ticket Cancellation

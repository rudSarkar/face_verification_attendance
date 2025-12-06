# Check-In/Check-Out Attendance System

## Overview
This system prevents students from leaving class early by implementing a **check-in/check-out** mechanism with minimum duration requirements.

## How It Works

### 1. **Check-In (Class Start)**
- Student arrives at class and uses face recognition to **check in**
- System records the check-in time
- Status: `Checked In`

### 2. **Check-Out (Class End)**
- Student uses face recognition to **check out** before leaving
- System calculates duration spent in class
- Compares duration against minimum required duration

### 3. **Attendance Determination**
- **Present**: Student stayed for minimum required duration (e.g., 45 out of 60 minutes)
- **Absent (Left Early)**: Student left before completing minimum duration
- **Checked In**: Student checked in but hasn't checked out yet

## Key Features

### Prevents Bunking
✅ Students cannot mark attendance and leave immediately  
✅ Duration tracking ensures minimum class participation  
✅ Early departures are flagged as "Absent (Left Early)"  

### Flexible Configuration
Each course can have:
- **Class Duration**: Total class time (default: 60 minutes)
- **Minimum Duration**: Required attendance time (default: 45 minutes)
- Customizable per course needs

### Example Scenarios

#### Scenario 1: Full Attendance ✅
- Check-in: 9:00 AM
- Check-out: 10:00 AM
- Duration: 60 minutes
- Minimum Required: 45 minutes
- **Status: Present**

#### Scenario 2: Left Early ❌
- Check-in: 9:00 AM
- Check-out: 9:30 AM
- Duration: 30 minutes
- Minimum Required: 45 minutes
- **Status: Absent (Left Early)**

#### Scenario 3: Just Enough ✅
- Check-in: 9:00 AM
- Check-out: 9:45 AM
- Duration: 45 minutes
- Minimum Required: 45 minutes
- **Status: Present**

## Database Schema Changes

### Attendance Table
```
- check_in_time: Time when student arrived
- check_out_time: Time when student left
- duration_minutes: Total minutes in class
- status: 'Checked In' | 'Present' | 'Absent (Left Early)'
```

### Courses Table
```
- class_duration_minutes: Total class duration (default: 60)
- min_duration_minutes: Minimum required (default: 45)
```

## Migration

### For Existing Databases
Run the migration script to update your database:

```bash
python migrate_database.py
```

This will:
1. Backup old attendance data
2. Create new table structure
3. Migrate existing records
4. Add duration fields to courses

### For New Installations
Simply run:
```bash
python database.py
```

The new schema will be created automatically.

## Usage Guide

### For Students

1. **At Class Start:**
   - Go to attendance page
   - Select your course
   - Click "✅ Check In"
   - Your face will be recognized
   - Confirmation: "Checked in successfully!"

2. **At Class End:**
   - Go to attendance page
   - Select same course
   - Click "🚪 Check Out"
   - Your face will be recognized
   - Status shown: "Present" or "Absent (Left Early)"

### For Instructors/Admins

1. **Adding a Course:**
   - Set course details
   - Configure **Class Duration** (e.g., 60 minutes)
   - Configure **Minimum Duration** (e.g., 45 minutes)
   - Students must stay 45+ minutes to be marked present

2. **Viewing Attendance:**
   - See check-in and check-out times
   - View duration spent in class
   - Filter by status (Present/Absent/Checked In)

3. **Reports:**
   - Export shows all timing details
   - Identify students leaving early
   - Track attendance patterns

## Benefits

### 1. **Fair System**
- No more "sign and run"
- Actual class participation tracked
- Transparent duration requirements

### 2. **Flexible**
- Different requirements per course
- Lab classes: longer duration
- Lectures: standard duration
- Seminars: custom duration

### 3. **Non-Disruptive**
- No interruptions during class
- Students check in/out at their own pace
- No fixed checkpoint times

### 4. **Accountable**
- Complete audit trail
- Exact times recorded
- Cannot game the system

## API Endpoints

### Check In
```javascript
POST /capture-attendance
{
    "course_code": "CS101",
    "action": "check_in"
}
```

### Check Out
```javascript
POST /capture-attendance
{
    "course_code": "CS101", 
    "action": "check_out"
}
```

## Status Codes

- `Checked In` - Student has checked in, not yet checked out
- `Present` - Completed minimum required duration
- `Absent (Left Early)` - Left before minimum duration
- `Absent` - Did not attend

## Best Practices

1. **Set Realistic Minimums**
   - Don't require 100% of class duration
   - Allow 10-15 minutes buffer
   - Example: 45 mins for 60-min class

2. **Clear Communication**
   - Inform students about requirements
   - Display minimum duration on attendance page
   - Show real-time status

3. **Grace Period**
   - Consider allowing a few minutes early departure
   - Emergency situations
   - Adjust minimums accordingly

## Troubleshooting

### "Already checked in"
- Student tried to check in twice
- Ask them to check out instead

### "No check-in record found"
- Student trying to check out without checking in
- Must check in first

### "Already checked out"
- Student already completed checkout
- Status already recorded

## Future Enhancements

Potential additions:
- SMS notifications for check-out reminders
- Real-time dashboard showing who's in class
- Automated reports for students below minimum
- Integration with LMS systems
- Mobile app for easier access

## Support

For issues or questions:
1. Check this documentation
2. Review database migration logs
3. Check application logs
4. Contact system administrator

---

**Version:** 2.0  
**Last Updated:** December 2025  
**Status:** Production Ready

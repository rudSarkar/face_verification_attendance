# Quick Start Guide - Check-In/Check-Out System

## For Students

### Step 1: Check In (When You Arrive)
1. Go to the attendance page
2. Select your course from the dropdown
3. Click **"Check In"** button
4. Look at the camera
5. Wait for face recognition
6. You'll see: "Checked in successfully!"

### Step 2: Attend Class
- Stay for at least the minimum required duration
- The duration is shown next to the course name
- Example: "CS101 - Programming (Min: 45 mins)"

### Step 3: Check Out (Before Leaving)
1. Go to the attendance page
2. Select the same course
3. Click **"Check Out"** button
4. Look at the camera
5. Wait for face recognition
6. You'll see your final status:
   - ✅ **"Present"** - You stayed long enough!
   - ⚠️ **"Absent (Left Early)"** - You left too early

## Important Rules

❌ **DON'T:**
- Check in and immediately leave
- Forget to check out
- Try to check in for someone else

✅ **DO:**
- Check in when you arrive
- Stay for minimum duration
- Check out before leaving
- Verify your status after checkout

## Status Meanings

- **Checked In** 🟡 - You're currently in class (haven't checked out yet)
- **Present** 🟢 - You completed the required duration
- **Absent (Left Early)** 🔴 - You left before completing minimum duration

## Example Timeline

**60-minute class, 45-minute minimum:**

```
9:00 AM  → Check In ✅
         ↓ (attend class)
9:45 AM  → Minimum time reached ✅
         ↓ (continue class)
10:00 AM → Check Out ✅
         → Status: Present 🟢
```

**If you leave early:**

```
9:00 AM  → Check In ✅
         ↓ (attend class)
9:30 AM  → Check Out ❌ (only 30 mins)
         → Status: Absent (Left Early) 🔴
```

## Troubleshooting

**"Already checked in"**
- You already checked in today
- Click "Check Out" instead

**"No check-in record found"**
- You didn't check in yet
- Check in first, then check out later

**"Face not recognized"**
- Make sure you're in good lighting
- Look directly at the camera
- Remove glasses/mask if needed
- Try again

## Tips for Success

1. **Arrive on time** - Check in right when class starts
2. **Stay focused** - Need to be present for minimum duration
3. **Don't forget** - Always check out before leaving
4. **Check status** - Verify you got "Present" status after checkout
5. **Good lighting** - Stand in well-lit area for face recognition

---

## For Instructors/Admins

### Setting Up a Course

1. Go to Admin Dashboard → Manage Courses → Add Course
2. Fill in course details:
   - Course Code: CS101
   - Course Name: Programming
   - Class Duration: 60 minutes (total class time)
   - Min Duration: 45 minutes (75% of class)
3. Set schedule and save

### Recommended Settings

**Standard Lecture (1 hour):**
- Class Duration: 60 minutes
- Min Duration: 45 minutes (75%)

**Lab Session (2 hours):**
- Class Duration: 120 minutes
- Min Duration: 90 minutes (75%)

**Seminar (90 minutes):**
- Class Duration: 90 minutes
- Min Duration: 70 minutes (~78%)

### Viewing Reports

1. Go to Admin Dashboard → View Attendance
2. You'll see:
   - Check-in time
   - Check-out time
   - Duration in class
   - Final status

3. Export to Excel for detailed analysis

### Common Scenarios

**Student forgot to check out:**
- Status shows "Checked In"
- Manually verify or ask student to check out next time

**System downtime:**
- Use manual attendance as backup
- Update system later

**Student emergency:**
- Can manually adjust status in database
- Or create exception policy

---

**Need Help?** Contact your system administrator.

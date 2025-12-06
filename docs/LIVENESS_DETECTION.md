# Anti-Spoofing Protection with Liveness Detection

## Overview

This system now includes **liveness detection** to prevent photo/picture spoofing attacks. The system uses **blink detection** to verify that the person in front of the camera is a real, live person rather than a photo, printed picture, or screen display.

## How It Works

### The Problem ❌
**Before:** Anyone could mark attendance by showing a photo
```
Student takes a photo of their friend
Shows the photo to the camera
System recognizes the face ✓
Attendance marked! ❌ (This is fraud!)
```

### The Solution ✅
**After:** Blink detection prevents photo spoofing
```
Student stands in front of camera
System detects face ✓
System monitors for eye blinks
Photo/picture shown → No blinks detected → REJECTED ❌
Real person → Natural blinking detected → VERIFIED ✓
```

## Technical Details

### Eye Aspect Ratio (EAR)
The system uses the **Eye Aspect Ratio** algorithm to detect blinks:

```
EAR = (||p2 - p6|| + ||p3 - p5||) / (2 * ||p1 - p4||)
```

Where p1-p6 are the eye landmark points.

- **Eyes open:** EAR ≈ 0.3
- **Eyes closed (blink):** EAR < 0.25

### Detection Process

1. **Face Detection:** dlib detects faces in the video frame
2. **Landmark Detection:** 68 facial landmarks are identified
3. **Eye Tracking:** Left and right eye regions (points 37-48) are monitored
4. **EAR Calculation:** Eye Aspect Ratio is calculated for both eyes
5. **Blink Detection:** When EAR drops below threshold for 2+ consecutive frames
6. **Verification:** At least 1 blink must be detected before attendance is marked

### Blink Detection Parameters

```python
EAR_THRESHOLD = 0.25           # Eye closure threshold
EAR_CONSEC_FRAMES = 2          # Frames with closed eyes to count as blink
MIN_BLINKS_REQUIRED = 1        # Minimum blinks for liveness verification
```

## Security Features

### ✅ Protections Added

1. **Photo Attack Prevention**
   - Printed photos cannot blink → Rejected
   - Phone screen photos cannot blink → Rejected
   
2. **Video Replay Prevention**
   - Pre-recorded videos show repetitive patterns → Can be detected
   - System requires natural blinking behavior
   
3. **Real-Time Verification**
   - Blink detection happens during live camera feed
   - User must be present in real-time

### ⚠️ Known Limitations

1. **High-Quality Video Replays**
   - Very high-quality video replays with natural blinking might pass
   - Consider adding challenge-response (e.g., "blink 3 times")
   
2. **Glasses/Sunglasses**
   - Dark glasses may interfere with eye detection
   - Users should remove sunglasses
   
3. **Poor Lighting**
   - Very dark environments may affect landmark detection
   - Adequate lighting is required

## User Experience

### Marking Attendance

1. **Select Course:** Choose the course from dropdown
2. **Face Camera:** Position face in camera view
3. **Blink Naturally:** System displays blink counter
4. **Verification:** When ≥1 blink detected, liveness is verified
5. **Mark Attendance:** Click Check In/Check Out

### Visual Feedback

- **Blink Counter:** Shows number of blinks detected
- **Liveness Status:**
  - ⚠️ Yellow box: "Please blink naturally" (not verified)
  - ✅ Green box: "Verified" (liveness confirmed)
- **Face Box Color:**
  - 🟠 Orange: Liveness not verified
  - 🟢 Green: Liveness verified

## Setup Instructions

### 1. Install Dependencies

```bash
pip install scipy imutils
```

These are already added to `requirements.txt`:
- `scipy` - For spatial distance calculations
- `imutils` - For face utilities

### 2. Download Facial Landmark Model

The system requires dlib's 68-point facial landmark predictor:

```bash
python download_model.py
```

This will download `shape_predictor_68_face_landmarks.dat` (~100 MB).

**Alternative manual download:**
```bash
wget http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2
bunzip2 shape_predictor_68_face_landmarks.dat.bz2
```

### 3. Enable/Disable Liveness Detection

Liveness detection is **enabled by default**. To disable:

```python
# In app.py
fr_system = FaceRecognitionSystem(enable_liveness=False)
```

## Testing

### Test Liveness Detection

Run the standalone test:

```bash
python liveness_detection.py
```

This will:
1. Open your webcam
2. Display real-time blink detection
3. Show EAR values
4. Count blinks over 5 seconds
5. Report pass/fail

### Test with Application

1. Start the application: `python app.py`
2. Go to "Mark Attendance"
3. Try these scenarios:

**✅ Should PASS:**
- Real person looking at camera and blinking naturally

**❌ Should FAIL:**
- Holding up a printed photo
- Showing a photo on phone screen
- Showing a photo on computer screen

## Architecture

### Components

```
┌─────────────────────────────────────────────────┐
│          liveness_detection.py                  │
│  - LivenessDetector class                       │
│  - Blink detection using EAR                    │
│  - Eye landmark tracking                        │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│     face_recognition_module.py                  │
│  - Integrates LivenessDetector                  │
│  - recognize_face_from_frame()                  │
│  - Returns: (student_id, confidence, location,  │
│              is_live)                           │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│              app.py                             │
│  - /video-feed: Shows blink counter             │
│  - /capture-attendance: Verifies blinks ≥ 1     │
│  - Rejects if liveness check fails              │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│      mark_attendance.html                       │
│  - Displays liveness status                     │
│  - Shows blink counter                          │
│  - Visual feedback (green/orange)               │
└─────────────────────────────────────────────────┘
```

### Flow Diagram

```
User opens mark attendance page
         ↓
Camera feed starts
         ↓
FaceRecognitionSystem initialized with LivenessDetector
         ↓
For each video frame:
    ├─→ Detect facial landmarks (68 points)
    ├─→ Extract eye regions (points 37-48)
    ├─→ Calculate EAR for both eyes
    ├─→ Compare EAR to threshold (0.25)
    ├─→ Count consecutive low-EAR frames
    └─→ If ≥2 frames: Increment blink counter
         ↓
Display blink count on video feed
         ↓
User clicks "Check In" or "Check Out"
         ↓
System checks: blink_count >= 1?
    ├─→ YES: Proceed with face recognition
    │         ↓
    │    Mark attendance ✅
    │
    └─→ NO: Reject attendance request
              ↓
         Show error: "Please blink naturally" ❌
```

## API Changes

### FaceRecognitionSystem.__init__()

```python
# Old
fr_system = FaceRecognitionSystem()

# New
fr_system = FaceRecognitionSystem(enable_liveness=True)
```

### recognize_face_from_frame()

```python
# Old return
(student_id, confidence, face_location)

# New return
(student_id, confidence, face_location, is_live)
```

### draw_face_box()

```python
# Old
draw_face_box(frame, location, student_id, confidence)

# New
draw_face_box(frame, location, student_id, confidence, is_live=True)
```

### /capture-attendance endpoint

```javascript
// Old request
{
  "course_code": "CS101",
  "action": "check_in"
}

// New request
{
  "course_code": "CS101",
  "action": "check_in",
  "blink_count": 2  // Blinks detected from video feed
}

// New error response
{
  "success": false,
  "message": "Liveness check failed. Please blink naturally and try again.",
  "liveness_required": true
}
```

## Troubleshooting

### "Failed to initialize liveness detector"

**Cause:** Missing `shape_predictor_68_face_landmarks.dat` file

**Solution:**
```bash
python download_model.py
```

### "No face detected" / Blinks not counting

**Possible causes:**
1. Poor lighting - Use better lighting
2. Face not in frame - Position face properly
3. Glasses/sunglasses - Remove dark glasses
4. Camera quality - Use better camera

### "Liveness check failed" when I am blinking

**Solutions:**
1. Blink more slowly and deliberately
2. Ensure face is well-lit
3. Look directly at camera
4. Remove glasses if wearing dark lenses

## Performance Considerations

### CPU Usage
- Facial landmark detection is CPU-intensive
- Expect 10-30% CPU usage during video feed
- Performance varies with camera resolution

### Optimization Tips
1. Lower camera resolution if needed
2. Reduce frame rate in video feed
3. Run on dedicated hardware for production

### Memory Usage
- Landmark model: ~100 MB on disk
- Runtime memory: ~50 MB additional

## Future Enhancements

### Possible Improvements

1. **Challenge-Response**
   - Random blink count requirement
   - "Please blink 3 times"
   - More secure than single blink

2. **Head Movement Detection**
   - Require slight head turn
   - Detects 3D depth
   - Harder to spoof with photos

3. **Texture Analysis**
   - Analyze image texture
   - Photos have different frequency patterns
   - Can detect screen moiré patterns

4. **3D Depth Sensing**
   - Use depth cameras (RealSense, iPhone FaceID)
   - Direct depth measurement
   - Most secure option

## Security Best Practices

1. **Regular Updates:** Keep dlib and opencv-python updated
2. **Monitor Logs:** Check for unusual patterns
3. **User Education:** Inform users about anti-spoofing
4. **Adjustable Thresholds:** Fine-tune EAR threshold for your environment
5. **Fallback Options:** Have manual verification for edge cases

## References

- [Eye Aspect Ratio Paper](https://vision.fe.uni-lj.si/cvww2016/proceedings/papers/05.pdf)
- [dlib Facial Landmarks](http://dlib.net/face_landmark_detection.py.html)
- [Face Anti-Spoofing: A Survey](https://arxiv.org/abs/1809.07172)

---

**Status:** ✅ Liveness Detection Active

**Security Level:** Medium-High (prevents basic photo attacks)

**User Impact:** Minimal (requires natural blinking)

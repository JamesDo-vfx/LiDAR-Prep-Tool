
# 🛸 JamesDo's Scan Aligner — LiDAR Prep Tool
**Author:** JamesDo | **Field:** VFX & Matchmove | 
---

*Simple and intuitive interface to help you process batch scan files quickly.*

---

## 🤔 What is this tool?

**JamesDo's Scan Aligner** is a Blender addon designed for Matchmove artists to process raw LiDAR scans (commonly from iPhones or specialized scanners). Instead of tedious manual repositioning and re-pivoting, this tool automates the workflow to ensure your models are perfectly placed at the **World Origin** with accurate scaling before being exported to software like 3DEqualizer, PFTrack, or Syntheyes. 

---

## ✨ Key Features

| Feature | Details |
| --- | --- |
| 📂 **Batch Import** | Import multiple `.fbx` files simultaneously with Shot/Sequence naming structures. |
| 📍 **Smart Registration** | Tools to snap Object Origins to the 3D Cursor instantly. |
| 📐 **Apply Transforms** | Automatically reset Location/Rotation to 0 and Scale to 1 to prevent tracking errors. |
| 📏 **Matchmove Scale** | Export options with x100 scaling specifically for Matchmove software. |
| 🚀 **Export Ready** | Export clean meshes with industry-standard coordinate alignment. |

---

## 🚀 Installation Guide

1. Download the addon `.zip` file from the [Releases](https://github.com/) section.
2. Open Blender, go to **Edit > Preferences > Add-ons**.
3. Click **Install...** and select the downloaded `.zip` file.
4. Check the box for **JamesDo's Scan Aligner** to activate it. 
---

## 🕹️ Usage Workflow

The tool is designed to be used from top to bottom in 3 easy steps:

### Step 1: Import Raw LiDAR Scan

* Click **Batch Import Scan** to select your raw scan files.
* The addon will automatically organize them into your Scene.

### Step 2: Scene Registration (Crucial Step)

To ensure Matchmove software interprets the space correctly, you need to clean the data:

![Workflow Preview](my_awesome_demo.mp4)

1. Identify a matching feature on both scans.
2. **Set Origin to Cursor** at that point for the source object.
3. Place the **3D Cursor** on the same corresponding point of the target object.
4. Use **Selection to Cursor** to snap them together perfectly. 
### Step 3: Export Aligned Model

1. Check the **Scale 100 (For MatchMove Software)** box if you are heading into 3DEqualizer or PFTrack.
2. Click **Export Mesh**.

---

## 🛠️ Troubleshooting

| Issue | Cause | Solution |
| --- | --- | --- |
| Model appears too small in 3DE | Scale 100 was not selected | Re-export and ensure the Scale 100 checkbox is ticked. |
| Heavy scan files, Blender freezes | High polygon count | Use a Decimate modifier to reduce the mesh before exporting. |
| Axis orientation is flipped | Different axis standards | Ensure the ground plane is on the XY axis before Applying Transforms. |

---

## 📄 License

Released under the MIT License — See the [LICENSE](https://www.google.com/search?q=LICENSE) file for more details.

---

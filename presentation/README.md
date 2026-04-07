# Energy Efficiency Advisor - LaTeX Presentation

## Files Required

### Images to Add (in `images/` folder)

1. **college_logo.png** - Your college logo (replace `bvrit_logo.jpg` in code if different name)
2. **app_interface.png** - Screenshot of main app interface
3. **architecture.png** - System architecture diagram
4. **results_screenshot.png** - Results page screenshot
5. **results_summary.png** - Summary section screenshot

### Screenshots to Capture

1. **app_interface.png** - Home form with appliances selected
2. **architecture.png** - Create a simple diagram showing: User → React → Gemini API → Results
3. **results_screenshot.png** - AI analysis results
4. **results_summary.png** - Summary cards showing kWh usage

## How to Compile

### Option 1: Overleaf (Recommended)
1. Upload all files to Overleaf
2. Upload your college logo as `college_logo.png` (or rename your logo)
3. Compile with XeLaTeX or PDFLaTeX

### Option 2: Local LaTeX
```bash
cd presentation
pdflatex main.tex
```

Make sure you have `beamer` installed:
```bash
# Ubuntu/Debian
sudo apt install texlive-latex-extra

# Mac
brew install --cask mactex

# Windows
# Install MiKTeX or TeX Live
```

## How to Customize

### 1. Add Your College Logo
Replace `college_logo` with your actual image name:
```latex
\node[anchor=north east, ...] at (current page.north east) {
    \includegraphics[width=0.8cm]{YOUR_LOGO_NAME}
};
```

### 2. Update Team Information
In the title frame, replace:
```latex
\author[]{%
    \textbf{Team Members:} \\
    Your Name 1 \\ Roll No: XXXXXXXX \\
    Your Name 2 \\ Roll No: XXXXXXXX
}
```

### 3. Update Guide Name
```latex
\textbf{Dr. [Guide Name]}
```

### 4. Update College Name
```latex
\textbf{[Your College Name]}
```

### 5. Add Screenshots
Place your screenshots in the `images/` folder:
- Rename them to match the filenames in the .tex file
- Or update the `\includegraphics{}` commands with your filenames

## Presentation Structure

1. **Title Slide** - Project title, team members, college info
2. **Table of Contents** - Overview of presentation
3. **Abstract** - Brief summary
4. **Problem Statement** - Why this project exists
5. **Introduction** - What the project does
6. **Objectives** - Goals of the project
7. **Technology Stack** - Tools and technologies used
8. **Implementation** - Modules and working process
9. **Results** - What the app produces
10. **Conclusion** - Summary and achievements
11. **Future Scope** - Potential enhancements
12. **References** - Sources cited
13. **Thank You** - End slide

## Tips

- Keep screenshots clear and readable
- Use high-resolution images (at least 1920x1080)
- Update all placeholder text with your actual information
- Test compile on Overleaf before final submission

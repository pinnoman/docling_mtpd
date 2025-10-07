# Batch Conversion Feature

## Overview
The batch conversion feature allows users to convert multiple documents simultaneously through the web interface, providing detailed results for each file including success/failure status.

## Implementation Details

### Backend (FastAPI)
- **New Endpoint**: `POST /convert-batch`
- **Location**: `backend/main.py`
- **Functionality**:
  - Accepts multiple files via `multipart/form-data`
  - Processes each file independently
  - Returns comprehensive results including:
    - Total files processed
    - Success/failure counts
    - Individual file results with content or error messages
  - Continues processing remaining files even if some fail

### Frontend (Next.js/React)

#### Components Modified/Created:

1. **FileUpload.tsx** (Modified)
   - Added `batchMode` prop to toggle between single and batch mode
   - Supports multiple file selection when in batch mode
   - Displays list of selected files with remove functionality
   - Dynamic button text based on mode and file count

2. **BatchConversionResult.tsx** (New)
   - Displays summary statistics (total, successful, failed)
   - Expandable/collapsible results for each file
   - Individual preview/raw view toggle for each result
   - Copy and download functionality per file
   - Bulk download all successful conversions
   - Color-coded success/failure indicators

3. **DocumentConverter.tsx** (Modified)
   - Added batch mode toggle switch
   - New `handleConvertBatch` function for batch API calls
   - Conditional rendering for single vs batch results
   - State management for batch results

4. **UI Components** (New)
   - `components/ui/switch.tsx` - Toggle switch component
   - `components/ui/label.tsx` - Label component
   - Both built with Radix UI primitives

### Dependencies Added
- `@radix-ui/react-switch`: ^1.0.3
- `@radix-ui/react-label`: ^2.0.2

## User Experience

### How to Use Batch Conversion:
1. Navigate to the Upload File tab
2. Toggle the "Batch Mode (Multiple Files)" switch
3. Select multiple files via:
   - File browser (supports multi-select)
   - Drag and drop multiple files
4. Review selected files (remove any if needed)
5. Click "Convert X File(s)" button
6. View results:
   - Summary shows total, successful, and failed conversions
   - Click on any file to expand and view its conversion
   - Toggle between preview and raw view for each file
   - Copy individual results or download them
   - Use "Download All" to get all successful conversions

### Features:
- **Error Handling**: Individual file failures don't stop the batch
- **Visual Feedback**: Clear success/failure indicators with icons
- **Flexible Output**: Preview or raw view for each converted document
- **Efficient Export**: Bulk download or individual file downloads
- **Progress Tracking**: See exactly which files succeeded or failed

## API Response Format

### Batch Conversion Response:
```json
{
  "success": true,
  "total": 3,
  "successful": 2,
  "failed": 1,
  "results": [
    {
      "filename": "document1.pdf",
      "success": true,
      "format": "markdown",
      "content": "# Converted content...",
      "error": null
    },
    {
      "filename": "document2.docx",
      "success": true,
      "format": "markdown",
      "content": "# More content...",
      "error": null
    },
    {
      "filename": "invalid.xyz",
      "success": false,
      "format": "markdown",
      "content": null,
      "error": "Unsupported file type: .xyz"
    }
  ]
}
```

## Testing Recommendations

1. **Single File**: Verify batch mode works with just one file
2. **Multiple Files**: Test with 3-5 files of different types
3. **Mixed Success**: Include both valid and invalid file types
4. **Large Batch**: Test with 10+ files to verify UI scalability
5. **Format Switching**: Change output format and re-convert
6. **Download All**: Verify bulk download creates correct files
7. **Error Cases**: Test with unsupported formats, corrupted files

## Future Enhancements

Potential improvements for future iterations:
- Progress bar showing conversion status in real-time
- Parallel processing for faster batch conversions
- Ability to pause/cancel batch operations
- Export batch results as a ZIP file
- Batch conversion from multiple URLs
- Save batch conversion history
- Retry failed conversions individually

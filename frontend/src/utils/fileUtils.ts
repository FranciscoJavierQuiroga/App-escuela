// src/utils/fileUtils.ts

/**
 * Downloads a file from a blob response
 * @param data Blob data from API response
 * @param filename Name of the file to download
 * @param type MIME type of the file
 */
export const downloadFile = (data: Blob, filename: string, type: string): void => {
  const blob = new Blob([data], { type });
  const url = window.URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.setAttribute('download', filename);
  
  // Append to the DOM
  document.body.appendChild(link);
  
  // Trigger the download
  link.click();
  
  // Clean up
  link.parentNode?.removeChild(link);
  window.URL.revokeObjectURL(url);
};

/**
 * Format a date string to a human-readable format
 * @param dateString ISO date string
 * @returns Formatted date string
 */
export const formatDate = (dateString: string): string => {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });
};

/**
 * Create a filename with timestamp
 * @param baseName Base name of the file
 * @param extension File extension
 * @returns Filename with timestamp
 */
export const createTimestampedFilename = (baseName: string, extension: string): string => {
  const now = new Date();
  const timestamp = [
    now.getFullYear(),
    String(now.getMonth() + 1).padStart(2, '0'),
    String(now.getDate()).padStart(2, '0'),
    String(now.getHours()).padStart(2, '0'),
    String(now.getMinutes()).padStart(2, '0'),
    String(now.getSeconds()).padStart(2, '0')
  ].join('');
  
  return `${baseName}_${timestamp}.${extension}`;
};

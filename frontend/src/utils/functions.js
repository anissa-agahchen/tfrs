import axios from 'axios';
import CONFIG from '../config';

const arrayMove = (arr, currentIndex, targetIndex) => {
  arr.splice(targetIndex, 0, arr.splice(currentIndex, 1)[0]);
  return arr;
};

const download = (url, params = {}) => (
  axios.get(url, {
    responseType: 'blob',
    params
  }).then((response) => {
    let filename = response.headers['content-disposition'].replace('attachment; filename=', '');
    filename = filename.replace(/"/g, '');

    const objectURL = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = objectURL;
    link.setAttribute('download', filename);
    document.body.appendChild(link);
    link.click();
  })
);

const getFileSize = (bytes) => {
  if (bytes === 0) {
    return '0 bytes';
  }

  const k = 1000;
  const sizes = ['bytes', 'KB', 'MB', 'GB', 'TB'];
  let i = Math.floor(Math.log(bytes) / Math.log(k));

  if (i > 4) { // nothing bigger than a terrabyte
    i = 4;
  }

  const filesize = parseFloat((bytes / k ** i).toFixed(1));

  return `${filesize} ${sizes[i]}`;
};

const getIcon = (mimeType) => {
  switch (mimeType) {
    case 'application/pdf':
      return 'file-pdf';
    case 'application/vnd.ms-excel':
    case 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
    case 'text/csv':
      return 'file-excel';
    case 'application/vnd.ms-powerpoint':
    case 'application/vnd.openxmlformats-officedocument.presentationml.presentation':
      return 'file-powerpoint';
    case 'application/msword':
    case 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
      return 'file-word';
    case 'image/gif':
    case 'image/jpg':
    case 'image/jpeg':
    case 'image/png':
      return 'file-image';
    case 'text/plain':
      return 'file-alt';
    default:
      return 'file-download';
  }
};

const getScanStatusIcon = (status) => {
  switch (status) {
    case 'PASS':
      return 'check';
    case 'FAIL':
      return 'times';
    default:
      return 'hourglass-half';
  }
};

const validateFiles = files => (
  files.filter((file) => {
    if (file.size > CONFIG.SECURE_DOCUMENT_UPLOAD.MAX_FILE_SIZE) {
      return false;
    }

    switch (file.type) {
      case 'application/msoutlook':
      case 'application/msword':
      case 'application/pdf':
      case 'application/vnd.ms-excel':
      case 'application/vnd.ms-powerpoint':
      case 'application/vnd.openxmlformats-officedocument.presentationml.presentation':
      case 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
      case 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
      case 'image/gif':
      case 'image/jpg':
      case 'image/jpeg':
      case 'image/png':
      case 'text/csv':
      case 'text/plain':
        return file.type;
      default:
        if (file.name.split('.').pop() === 'xls' || file.name.split('.').pop() === 'ppt' ||
          file.name.split('.').pop() === 'doc') {
          return file;
        }

        return false;
    }
  })
);

export { arrayMove, download, getFileSize, getIcon, getScanStatusIcon, validateFiles };

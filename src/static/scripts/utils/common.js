/**
 * Change the favicon based on the current browser theme used
 */
if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
  let link = document.createElement('link')
  link.rel = 'icon';
  link.href = 'static/res/CloudComputingFaviconLight.svg';
  document.head.append(link);
} else {
  let link = document.createElement('link')
  link.rel = 'icon';
  link.href = 'static/res/CloudComputingFaviconDark.svg';
  document.head.append(link);
}
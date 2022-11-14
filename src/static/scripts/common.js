if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
    console.log("Dark mode on");
    let link = document.createElement('link')
    link.rel = 'icon';
    link.href = 'static/res/CloudComputingFaviconLight.svg';
    document.head.append(link);
  } else {
    console.log("Light mode on");
      let link = document.createElement('link')
    link.rel = 'icon';
    link.href = 'static/res/CloudComputingFaviconDark.svg';
    document.head.append(link);
  }

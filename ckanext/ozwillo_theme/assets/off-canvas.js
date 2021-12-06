document.addEventListener('DOMContentLoaded', function() {
  document.getElementById('toggle-toc').addEventListener('click', function() {
    var el = document.body, className = 'toc-open';
    if (el.classList) {
      el.classList.toggle(className);
    } else {
      var classes = el.className.split(' ');
      var existingIndex = classes.indexOf(className);

      if (existingIndex >= 0)
        classes.splice(existingIndex, 1);
      else
        classes.push(className);

      el.className = classes.join(' ');
    }
  });
});
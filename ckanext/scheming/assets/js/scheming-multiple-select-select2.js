this.ckan.module('scheming-multiple-select-select2', function(jQuery) {
  return {
    options: {
      field: null
    },
    initialize: function () {
      var field = this.options.field;
      $(this.el).ready(function() {
        // initialize select as Select2
        $(`#field-${field}`).select2();
          
          // Set the width of the parent divs of the Select2 element to 100%
        $(`#s2id_field-${field}`).css('width', '100%');
      });
    },
  };
});
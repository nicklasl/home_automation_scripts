Date.prototype.yyyymm = function() {
  var mm = this.getMonth() + 1; // getMonth() is zero-based

  return [this.getFullYear(),
          (mm>9 ? '' : '0') + mm
         ].join('');
};

Date.prototype.yyyy = function() {
  return [this.getFullYear()].join('');
};

Date.prototype.mm = function() {
  var mm = this.getMonth() + 1; // getMonth() is zero-based
  return [(mm>9 ? '' : '0') + mm].join('');
};

var date = new Date();
console.log(date.yyyymm());
console.log(date.yyyy());
console.log(date.mm());

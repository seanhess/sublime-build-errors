var C1 = (function () {
    function C1() {
        this.pubProp = 0;
        this.privProp = 0;
    }
    C1.prototype.pubMeth = function () {
        this.pubMeth();
    };
    C1.prototype.privMeth = function () {
    };

    C1.prototype.testMeth = function () {
        this.pubMeth();
        return this;
    };
    C1.prototype.testMeth2 = function (a, b) {
        return a - b;
    };
    return C1;
})();

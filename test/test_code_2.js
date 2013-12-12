///<reference path='test_dep.ts'/>
var Test = (function () {
    function Test() {
    }
    Test.prototype.test = function () {
        console.log("oh hai");
    };
    Test.prototype.test_2 = function (a, b) {
        return a + b;
    };
    return Test;
})();

var v = new C1();
var a = v.testMeth2(12, 15);
var t = new Test();
v.pubMeth();
v.badMethod();
var v2 = new C1();

var henry = "hello";

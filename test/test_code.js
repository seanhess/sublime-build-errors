var Foo;
(function (Foo) {
    var testing = "";
})(Foo || (Foo = {}));

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
    return C1;
})();

var f = new C1();
f.pubMeth(); // test on F.

var M;
(function (M) {
    var C = (function () {
        function C() {
            this.pub = 0;
            this.priv = 1;
            this.test = 123;
        }
        return C;
    })();
    M.C = C;
    M.V = 0;
})(M || (M = {}));

var c = new M.C();
c.test;

var Greeter = (function () {
    function Greeter(message) {
        this.greeting = message;
    }
    Greeter.prototype.greet = function () {
        return "Hello, " + this.greeting;
    };

    Greeter.prototype.test = function (a, b) {
        return a + " " + b;
    };
    return Greeter;
})();

var greeter = new Greeter("world");
greeter.greet();
greeter.test("lol", "hh");
var gr2 = new Greeter("haha");

var button = document.createElement('button');
button.innerText = "Say Hello";
button.onclick = function () {
    alert(greeter.greet());
};

document.body.appendChild(button);

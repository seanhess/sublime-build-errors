var Foo;
(function (Foo) {
    var testing = "";
})(Foo || (Foo = {}));

var C2 = (function () {
    function C2() {
        this.pubProp = 0;
        this.privProp = 0;
    }
    C2.prototype.pubMeth = function () {
        this.pubMeth();
    };
    C2.prototype.privMeth = function () {
    };

    C2.prototype.testMeth = function () {
        this.pubMeth();
        return this;
    };
    return C2;
})();

var f = new C2();
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

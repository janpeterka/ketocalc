function getEl(el) {
    return document.getElementById(el);
}

function setEl(el, what) {
    document.getElementById(el).innerHTML = what;
}

function print(string) {
    console.log(string);
}

Math.rand = function(min, max) {
    return Math.floor(Math.random() * (max - min) + min);
};

Math.chance = function(chance) {
    if (Math.rand(1, 10000) < (chance * 100)) {
        return true;
    } else {
        return false;
    }
};

Math.clamp = function(val, min, max) {
    return Math.min(Math.max(val, min), max);
};

Number.prototype.clamp = function(min, max) {
    return Math.min(Math.max(this, min), max);
};

Number.prototype.isBetween = function(min, max) {
    if (this == Math.min(Math.max(this, min), max)) {
        return true;
    } else {
        return false;
    }
};

Math.isBetween = function(val, min, max) {
    if (val == Math.clamp(val, min, max)) {
        return true;
    } else {
        return false;
    }
};

function decToHex(d) {
    return ("0" + (Number(d).toString(16))).slice(-2).toUpperCase();
}
Array.prototype.random = function() {
    return this[Math.rand(0, this.length)];
};

Array.prototype.shuffle = function() {
    var currentIndex = this.length,
        temporaryValue, randomIndex;

    // While there remain elements to shuffle...
    while (0 !== currentIndex) {

        // Pick a remaining element...
        randomIndex = Math.floor(Math.random() * currentIndex);
        currentIndex -= 1;

        // And swap it with the current element.
        temporaryValue = this[currentIndex];
        this[currentIndex] = this[randomIndex];
        this[randomIndex] = temporaryValue;
    }

    return this;
};
/*
Middle height (average) of 2 or 4 height
 */

function midH(e, f, g, h) {
    g = g || 0;
    h = h || 0;
    if (g === 0 && h === 0) {
        return (e.height + f.height);
    } else {
        return ((e.height + g.height) / 2 + (h.height + f.height) / 2) / 2;
    }
}

/*
Random between two/four numbers
 */
function randMidH(a, b, c, d) {
    c = c || -1;
    d = d || -1;
    if (c == -1 && d == -1) {
        return Math.rand(Math.min(a.height, b.height), Math.max(a.height, b.height));
    } else if (d == -1) {
        return Math.rand(Math.min(a.height, b.height, c.height), Math.max(a.height, b.height, c.height));
    } else {
        return Math.rand(Math.min(a.height, b.height, c.height, d.height),
            Math.max(a.height, b.height, c.height, d.height));
    }
}

function heightComparator(a, b) {
    if (a.height < b.height) {
        return -1;
    }
    if (a.height > b.height) {
        return 1;
    }
    return 0;
}
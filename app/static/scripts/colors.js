const getDominant = (url) => {
    const img = new Image();
    img.crossOrigin = 'Anonymous';
    img.src = url;
    img.onload = () => {
        const colorThief = new ColorThief();
        // const color = colorThief.getColor(img);
        let colors = colorThief.getPalette(img, 2);
        colors = colors.map((element) => {
            return element.map((element) => {
                return element.toString(16).padStart(2, '0');
            }).join('');
        });
        let color = getFurthestColor(...colors);
        color = color.match(/.{1,2}/g).map((element) => {
            return parseInt(element, 16);
        });
        console.log(color, colors);
        const rgb = `rgb(${color[0]}, ${color[1]}, ${color[2]})`;
        document.querySelector(':root').style.setProperty('--primary-color', rgb);
        let quoficients = [0.2126, 0.7152, 0.0722];
        let luminance = 0;
        color.forEach((element, index) => {
            element /= 255;
            element = element < 0.03928 ? element / 12.92 : Math.pow((element + 0.055) / 1.055, 2.4);
            luminance += element * quoficients[index];
        });
        let darker = color;
        let lighter = color;
        if (luminance > 0.5) {
            console.log(color)
            const darker = color.map((element) => {
                element = element / 255;
                element = element < 0.03928 ? element / 12.92 : Math.pow((element + 0.055) / 1.055, 2.4);
                element = element - 0.3;
                element = element < 0.03928 ? element * 12.92 : 1.055 * Math.pow(element, 1 / 2.4) - 0.055;
                element = element * 255;
                element = element < 0 ? 0 : element > 255 ? 255 : element; // Check and limit the range of the output value
                console.log(element);
                return element;
            });
            lighter = color;
            console.log(`light => lighter: ${lighter}, darker: ${darker}`);
            document.querySelector(':root').style.setProperty('--primary-color', darker ? `rgb(${darker[0]}, ${darker[1]}, ${darker[2]})` : '#0b8e5e');
            document.querySelector(':root').style.setProperty('--primary-color-light', rgb ? rgb : '#10c28e');
        } else {
            lighter = color.map((element) => {
                element = element / 255;
                element = element < 0.03928 ? element / 12.92 : Math.pow((element + 0.055) / 1.055, 2.4);
                element = element + 0.3;
                element = element < 0.03928 ? element * 12.92 : 1.055 * Math.pow(element, 1 / 2.4) - 0.055;
                element = element * 255;
                return element;
            });

            darker = color;
            console.log(`dark => lighter: ${lighter}, darker: ${darker}`);
            document.querySelector(':root').style.setProperty('--primary-color-light', lighter ? `rgb(${lighter[0]}, ${lighter[1]}, ${lighter[2]})` : '#10c28e');
            document.querySelector(':root').style.setProperty('--primary-color', rgb ? rgb : '#0b8e5e');
        }


        console.log(darker[0] * 0.299 + darker[1] * 0.587 + darker[2] * 0.114)
        if (darker[0] * 0.299 + darker[1] * 0.587 + darker[2] * 0.114 > 186) {
            document.querySelector(':root').style.setProperty('--contrast-color', 'black');
        } else {
            document.querySelector('body.dark').style.setProperty('--sidebar-contrast-color', 'white');
            document.querySelector(':root').style.setProperty('--contrast-color', 'white');
        }
    }
}

function getFurthestColor(color1, color2) {
    // Convert colors to HSL values
    const hsl1 = hexToHsl(color1);
    const hsl2 = hexToHsl(color2);

    // Calculate difference in lightness for each color
    const lightness1 = hsl1.l;
    const lightness2 = hsl2.l;
    const delta1 = Math.abs(lightness1 - 0.5);
    const delta2 = Math.abs(lightness2 - 0.5);

    // Return the color with the maximum difference in lightness
    return delta1 > delta2 ? color1 : color2;
}

function hexToHsl(hex) {
    // Convert hex color to HSL
    const r = parseInt(hex.substr(1, 2), 16) / 255;
    const g = parseInt(hex.substr(3, 2), 16) / 255;
    const b = parseInt(hex.substr(5, 2), 16) / 255;
    const max = Math.max(r, g, b);
    const min = Math.min(r, g, b);
    const delta = max - min;
    let h, s, l;
    if (delta === 0) {
        h = 0;
    } else if (max === r) {
        h = ((g - b) / delta) % 6;
    } else if (max === g) {
        h = (b - r) / delta + 2;
    } else {
        h = (r - g) / delta + 4;
    }
    h = Math.round(h * 60);
    if (h < 0) h += 360;
    l = (max + min) / 2;
    if (delta === 0) {
        s = 0;
    } else {
        s = delta / (1 - Math.abs(2 * l - 1));
    }
    s = Math.round(s * 100);
    l = Math.round(l * 100);
    return { h, s, l };
}

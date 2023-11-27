// G translate if you're looking at this, I know you're using the Google translation Widget
// https://developers.google.com/search/blog/2020/05/google-translates-website-translator


// I don't actually want the toolbar to show up, don't give it anything to attach to

//const div = document.createElement("div");
//div.className = "gtranslate_wrapper";
//document.body.appendChild(div);

// Set the language based off the URL
language = new URLSearchParams(window.location.search).get('lang');
if (language != null) {
    // For some reason cookies must be set on domain and subdomain
    document.cookie = `googtrans=/auto/${language};`;
    document.cookie = `googtrans=/auto/${language}; domain=koyeb.app`;
    // Google yaps that performance.measure is negative because we display the page several times due to embeds
    // The performance measure they use returns a negative this way, so here I just disable performance measure builtin
    performance.measure = null
//    document.addEventListener("DOMContentLoaded", () => {
        const script = document.createElement('script');
        script.src = "https://cdn.gtranslate.net/widgets/latest/float.js";
        document.body.appendChild(script);
//    });
}

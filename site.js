// 明暗の切り替え、名前の横のリンクの開け閉め、制作物のページの動画
(function () {
  var root = document.documentElement;

  var theme = document.querySelector(".theme");
  function syncTheme() {
    theme.setAttribute("aria-pressed", root.dataset.theme === "dark" ? "true" : "false");
  }
  if (theme) {
    syncTheme();
    theme.addEventListener("click", function () {
      var next = root.dataset.theme === "dark" ? "light" : "dark";
      root.dataset.theme = next;
      try { localStorage.setItem("theme", next); } catch (e) {}
      syncTheme();
    });
  }

  var more = document.querySelector(".more");
  if (more) {
    more.addEventListener("click", function () {
      var open = more.getAttribute("aria-expanded") !== "true";
      more.setAttribute("aria-expanded", String(open));
      more.setAttribute("aria-label", open ? "リンクを隠す" : "リンクを表示");
      document.getElementById(more.getAttribute("aria-controls")).hidden = !open;
    });
  }

  // 画面に入ったら、音を消して再生する。動きを減らす設定のときは自動では再生しない
  var video = document.querySelector(".player video");
  if (video && !matchMedia("(prefers-reduced-motion: reduce)").matches) {
    new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) video.play().catch(function () {});
        else video.pause();
      });
    }, { threshold: 0.6 }).observe(video);
  }
})();

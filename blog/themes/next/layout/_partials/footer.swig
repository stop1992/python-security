<div class="copyright" >
  {% set current = date(Date.now(), "YYYY") %}
  &copy; {% if theme.since and theme.since != current %} {{ theme.since }} - {% endif %}
  <span itemprop="copyrightYear">{{ current }}</span>
  <span class="with-love">
    <i class="fa fa-heart"></i>
  </span>
  <span class="author" itemprop="copyrightHolder">{{ config.author }}</span>
</div>

<script async src="https://dn-lbstatics.qbox.me/busuanzi/2.3/busuanzi.pure.mini.js">
</script>
<span id="busuanzi_container_site_pv">
    总访问量<span id="busuanzi_value_site_pv"></span>次
</span>
<span id="busuanzi_container_site_uv">
  访客数<span id="busuanzi_value_site_uv"></span>人次
</span>

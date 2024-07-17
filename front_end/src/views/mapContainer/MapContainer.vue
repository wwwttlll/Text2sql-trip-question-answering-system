<template>
  <div id="map-container" ref="mapContainer"></div>
</template>

<script>
export default {
  name: 'MapContainer',
  mounted() {
    this.initMap();
  },
  methods: {
    initMap() {
      const latitude = parseFloat(this.$route.query.latitude);
      const longitude = parseFloat(this.$route.query.longitude);
      console.log(latitude)
      console.log(longitude)
      const map = new AMap.Map(this.$refs.mapContainer, {
        viewMode: '3D', // 使用2D视图
        zoom: 11, // 初始化地图级别
        center: [latitude,longitude] // 使用 URL 参数中的经纬度作为地图中心点
      });

      const marker = new AMap.Marker({
        position: [latitude,longitude], // 使用 URL 参数中的经纬度作为标记位置
        map: map, // 添加到地图实例中
        icon: 'https://a.amap.com/jsapi_demos/static/demo-center/icons/poi-marker-default.png' // 标记图标 URL
      });
    }
  }
}
</script>

<style scoped>
#map-container {
  width: 100%;
  height: 100vh;
}
</style>

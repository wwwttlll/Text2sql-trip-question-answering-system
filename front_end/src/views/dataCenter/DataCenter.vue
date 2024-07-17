<template>
  <el-container class="home-container">
    <el-header>
      <div class="header-left">
        <img src="@/assets/earth.png" alt="" height="50px" />
      </div>
    </el-header>
    <el-container>
      <el-aside width="200px">
        <el-menu background-color="#545c64" text-color="#fff" active-text-color="#ffd04b">
          <el-menu-item index="1" @click="goToHome">
            <i class="el-icon-menu"></i>
            <span slot="title">首页</span>
          </el-menu-item>
          <el-menu-item index="2" @click="goToWeather">
            <i class="el-icon-search"></i>
            <span slot="title">天气查询</span>
          </el-menu-item>
          <el-menu-item index="3">
            <i class="el-icon-data-line"></i>
            <span slot="title">旅游信息查询</span>
          </el-menu-item>
          <el-menu-item index="4" @click="logout">
            <i class="el-icon-switch-button"></i>
            <span slot="title">退出</span>
          </el-menu-item>
        </el-menu>
      </el-aside>
      <div class="box">
        <div class="title">
          <img src="" alt class="logo" />
          <span class="title-hn">旅游信息查询</span>
        </div>
        <div class="search-section">
          <el-select v-model="selectedTable" placeholder="请选择你需要查询的领域" @change="handleTableChange">
            <el-option label="酒店信息" value="hotel"></el-option>
            <el-option label="景点信息" value="scenic_area"></el-option>
            <el-option label="特产信息" value="specialty"></el-option>
          </el-select>
          <el-input v-model="searchQuery" placeholder="请输入搜索关键词" style="width: 1100px;"></el-input>
          <el-button @click="search">搜索</el-button>
        </div>
        <div class="results-section" v-if="paginatedResults.length">
          <el-table :data="paginatedResults">
            <!-- 酒店表格列 -->
            <template v-if="selectedTable === 'hotel'">
              <el-table-column prop="hotel_name" label="酒店名"></el-table-column>
              <el-table-column prop="hotel_ads" label="酒店地址"></el-table-column>
              <el-table-column prop="score" label="酒店评分"></el-table-column>
              <el-table-column prop="province" label="省"></el-table-column>
              <el-table-column prop="city" label="市"></el-table-column>
            </template>
            <!-- 景点表格列 -->
            <template v-else-if="selectedTable === 'scenic_area'">
              <el-table-column prop="view_name" label="景点名"></el-table-column>
              <el-table-column prop="level" label="景点等级"></el-table-column>
              <el-table-column prop="province" label="省"></el-table-column>
              <el-table-column prop="city" label="市"></el-table-column>
              <el-table-column label="具体坐标">
                <template slot-scope="scope">
                  <el-button type="text" @click="showMap(scope.row)">查看</el-button>
                </template>
              </el-table-column>
            </template>
            <!-- 特产表格列 -->
            <template v-else-if="selectedTable === 'specialty'">
              <el-table-column prop="specialty_name" label="特产名"></el-table-column>
              <el-table-column prop="specialty_link" label="介绍网址"></el-table-column>
              <el-table-column prop="city" label="市"></el-table-column>
              <el-table-column prop="province_area" label="地区"></el-table-column>
            </template>
          </el-table>
          <el-pagination @current-change="handleCurrentChange" :current-page="currentPage" :page-size="pageSize"
            :total="results.length" layout="total, prev, pager, next"></el-pagination>
        </div>
      </div>
    </el-container>
  </el-container>
</template>

<script>
import axiosInstance from '@/utils/axiosInstance';

export default {
  data() {
    return {
      searchQuery: '',
      selectedTable: '',
      results: [],
      currentPage: 1,
      pageSize: 7,
    };
  },
  computed: {
    paginatedResults() {
      const start = (this.currentPage - 1) * this.pageSize;
      const end = this.currentPage * this.pageSize;
      return this.results.slice(start, end);
    },
  },
  methods: {
    logout() {
      window.sessionStorage.clear();
      this.$router.push('/login');
    },
    goToWeather() {
      this.$router.push('/weather');
    },
    goToHome() {
      this.$router.push('/home');
    },
    async search() {
      try {
        const token = sessionStorage.getItem('token');
        console.log("token:", token);
        const config = {
          headers: {
            token: token // 使用自定义头 'token'
          }
        };
        let url = `/search/${this.selectedTable}?searchQuery=${encodeURIComponent(this.searchQuery)}`;
        console.log("url:", url);
        console.log("config:", config);
        const response = await axiosInstance.post(url, null, config,{timeout:5000});
        console.log("response data:", response.data);
        if (response.data.code === 200) {
          this.results = response.data.data;
        } else {
          console.error("Backend error:", response.data.msg || "Unknown error");
          this.results = [];
        }
      } catch (error) {
        console.error("Error fetching search results:", error);
        this.results = [];
      }
    },
    handleTableChange() {
      this.searchQuery = '';
      this.results = [];
    },
    handleCurrentChange(page) {
      this.currentPage = page;
    },
    showMap(scenicSpot) {
        // 导航到另一个页面，并将景点的经纬度作为参数传递
        this.$router.push({
            path: '/mapContainer', // 这里是你的地图页面路径
            query: {
                latitude: scenicSpot.latitude,
                longitude: scenicSpot.longitude
            }
        });
    }
  },
};
</script>

<style scoped>
.box {
  width: 95%;
  height: 100%;
  background-color: #fafafa;
  position: relative;
  padding-top: 0;
  padding-right: 20px;
  padding-bottom: 20px;
  padding-left: 20px;
  margin: 0 auto;
}

.title-hn {
  display: flex;
  font-size: 25px;
  color: #333;
  align-items: center;
  justify-content: center;
  line-height: 120px;
}

.search-section {
  margin: 20px 0;
  display: flex;
  align-items: center;
}

.results-section {
  margin-top: 20px;
}

.el-header {
  background-color: #545c64;
  display: flex;
  justify-content: space-between;
  padding-left: 0;
  align-items: center;
  color: #fff;
  font-size: 20px;
}

.header-left {
  display: flex;
  align-items: center;
  padding-left: 20px;
  /* 向右移动图片 */
}

.home-container {
  height: 100%;
}

.el-aside {
  background-color: #545c64;
  /* 确保整个侧边栏区域都有背景色 */
  height: 92.8vh;
}
</style>

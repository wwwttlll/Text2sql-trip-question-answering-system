<template>
    <el-container class="main-container">
        <el-header>
            <div class="header-left">
                <img src="@/assets/earth.png" alt="" height="50px" />
            </div>
        </el-header>
        <el-container class="content-container">
            <el-aside width="200px" class="side-menu">
                <el-menu background-color="#545c64" text-color="#fff" active-text-color="#ffd04b">
                    <el-menu-item index="1" @click="goToHome">
                        <i class="el-icon-menu"></i>
                        <span slot="title">首页</span>
                    </el-menu-item>
                    <el-menu-item index="2">
                        <i class="el-icon-search"></i>
                        <span slot="title">天气查询</span>
                    </el-menu-item>
                    <el-menu-item index="3" @click="goToDataCenter">
                        <i class="el-icon-data-line"></i>
                        <span slot="title">旅游信息查询</span>
                    </el-menu-item>
                    <el-menu-item index="4" @click="logout">
                        <i class="el-icon-switch-button"></i>
                        <span slot="title">退出</span>
                    </el-menu-item>
                </el-menu>
            </el-aside>
            <el-main class="main-content">
                <div class="title">
                    <img src="" alt class="logo" />
                    <span class="title-hn">全国天气查询</span>
                </div>
                <el-input v-model="input" placeholder="输入位置并按下回车以查询该地天气" @keyup.enter.native="keyUp"></el-input>
                <p class="ipAddress">
                    <i class="el-icon-location-outline"></i>{{ ipAddress }}
                    <el-link type="primary" @click="useIp">使用该地区</el-link>
                </p>
                <el-divider></el-divider>
                <div class="showBlock">
                    <p class="address">{{ address }}</p>
                    <p class="temperature">{{ temperature }}℃<span class="weather">{{ weather }}
                            <span><i class="mainWeather" :class="getIcon"></i></span>
                        </span></p>
                    <div class="other">
                        <p class="wind">
                            <i class="el-icon-wind-power"></i> 风向: <span>{{ winddirection
                                }}</span>&nbsp;&nbsp;&nbsp;<span>风力: {{ windpower }}级</span>
                        </p>
                        <p class="humidity"><i class="el-icon-odometer"></i> 湿度: {{ humidity }}</p>
                        <p id="reporttime">消息发布时间: {{ reporttime }}</p>
                    </div>
                </div>
            </el-main>
        </el-container>
    </el-container>
</template>

<script>
export default {
    name: 'Weather',
    data() {
        return {
            input: '',
            city: '',
            adcode: '',
            address: '',
            ipAddress: '',
            ipAdCode: '',
            weather: '',
            temperature: '',
            winddirection: '',
            windpower: '',
            humidity: '',
            reporttime: '',
            icon: true,
        };
    },
    watch: {
        adcode() {
            if (!this.adcode) return;

            this.$axios.get('https://restapi.amap.com/v3/weather/weatherInfo', {
                params: {
                    key: '3ba63aaaa0ce57cbd34e1a5c26f8273f',
                    city: this.adcode,
                    extensions: 'base',
                },
            }).then(response => {
                const lives = response.data.lives[0];
                this.weather = lives.weather;
                this.temperature = lives.temperature;
                this.winddirection = lives.winddirection;
                this.windpower = lives.windpower;
                this.humidity = lives.humidity;
                this.reporttime = lives.reporttime;
                this.address = lives.city;

                localStorage.setItem('adcode', this.adcode);
            }).catch(error => {
                this.$notify.info({
                    title: '未知错误',
                    message: error.message,
                });
            });
        },
    },
    computed: {
        getIcon() {
            this.icon = false;
            if (this.weather.includes('晴')) {
                return 'el-icon-sunny';
            } else if (this.weather.includes('多云')) {
                return 'el-icon-cloudy-and-sunny';
            } else if (this.weather.includes('阴')) {
                return 'el-icon-partly-cloudy';
            } else if (this.weather.includes('雨')) {
                return 'el-icon-heavy-rain';
            } else if (this.weather.includes('雪')) {
                return 'el-icon-light-rain';
            }
            this.icon = true;
        },
    },
    methods: {
        useIp() {
            this.adcode = this.ipAdCode;
        },
        keyUp() {
            this.city = this.input;
            this.input = '';
            this.getCityCode();
        },
        getIp() {
            this.$axios.get('https://restapi.amap.com/v3/ip', {
                params: {
                    key: '3ba63aaaa0ce57cbd34e1a5c26f8273f',
                },
            }).then(response => {
                this.ipAddress = `${response.data.province}${response.data.city}`;
                this.ipAdCode = response.data.adcode;

                if (!localStorage.getItem('adcode')) {
                    this.adcode = response.data.adcode;
                }
            }).catch(error => {
                this.$notify.info({
                    title: 'IP 地址获取错误',
                    message: error.message,
                });
            });
        },
        getCityCode() {
            this.$axios.get('https://restapi.amap.com/v3/geocode/geo', {
                params: {
                    key: '3ba63aaaa0ce57cbd34e1a5c26f8273f',
                    address: this.city,
                },
            }).then(response => {
                if (response.data.status === '1') {
                    this.adcode = response.data.geocodes[0].adcode;
                } else {
                    this.$notify.error({
                        title: '查询错误',
                        message: '请重新核对查询地址',
                    });
                }
            }).catch(error => {
                this.$notify.error({
                    title: '查询错误',
                    message: error.message,
                });
            });
        },
        logout() {
            window.sessionStorage.clear();
            this.$router.push('/login');
        },
        goToHome() {
            this.$router.push('/home');
        },
        goToDataCenter() {
            this.$router.push('/dataCenter');
        },
    },
    mounted() {
        if (localStorage.getItem('adcode')) {
            this.adcode = localStorage.getItem('adcode');
        }
        this.getIp();
    },
};
</script>

<style scoped>
.full-container {
    height: 100vh;
    width: 100vw;
    display: flex;
    flex-direction: row;
}

.title {
    display: flex;
    font-size: 25px;
    color: #333;
    align-items: center;
    justify-content: center;
    line-height: 120px;
}

.side-menu {
    background-color: #545c64;
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

.main-container {
    height: 100vh;
    /* 修改高度为100vh，使其撑满整个视口 */
    width: 100%;
    /* 宽度设置为100% */
    display: flex;
    flex-direction: column;
}

.content-container {
    flex: 1;
    /* 设置主体内容容器为弹性项，使其占据剩余空间 */
}

.main-content {
    padding: 20px;
    overflow-y: auto;
}

.ipAddress {
    margin-top: 10px;
}

.showBlock {
    margin-top: 10px;
}

.temperature {
    font-size: 50px;
    margin-left: 50px
}

.weather {
    margin-left: 70px;
    font-size: 50px;
}

.address {
    font-size: 20px;
}

.other {
    margin-top: 10px;
}

.other p {
    margin-top: 10px;
    font-size: 18px;
}

#reporttime {
    margin-top: 10px;
    font-size: 14px;
}

.mainWeather {
    float: right;
    margin-top: -25px;
    margin-right: 60%;
    font-size: 120px;
}

.showBlock {
    margin-left: 10px;
}
</style>
您
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
          <el-menu-item index="1">
            <i class="el-icon-menu"></i>
            <span slot="title">首页</span>
          </el-menu-item>
          <el-menu-item index="2" @click="goToWeather">
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
      <div class="box">
        <div class="title">
          <img src="" alt class="logo" />
          <span class="title-hn">智能地理知识问答系统</span>
        </div>
        <div id="content" class="content">
          <div v-for="(item, index) in info" :key="index">
            <div class="info_r info_default" v-if="item.type == 'leftinfo'">
              <span class="circle circle_r">
                <img :src="robotAvatar" alt="机器人头像" class="avatar" />
              </span>
              <div class="con_r con_text">
                <div v-html="item.content"></div>
                <div v-if="item.sql" class="sql-output">
                  <h3>生成的SQL查询：</h3>
                  <p>{{ item.sql }}</p>
                </div>
                <el-button
                  v-if="item.mode === 'text2Sql' && item.content && item.content !== '您好，欢迎使用智能地理知识问答系统!' && item.content !== '退出'"
                  @click="downloadTable(item.content)" class="buttonsend">
                  <span style="vertical-align: 4px;">下载表格</span>
                </el-button>
                <div v-for="(item2, index) in item.question" :key="index">
                  <div class="con_que" @click="clickRobot(item2.content, item2.id)">
                    <div class="czkj-question-msg">
                      {{ item2.index }}
                      {{ item2.content }}
                    </div>
                  </div>
                </div>
              </div>
              <div class="time_r">{{ item.time }}</div>
            </div>
            <div class="info_l" v-if="item.type == 'rightinfo'">
              <div class="con_r con_text">
                <span class="con_l">{{ item.content }}</span>
                <span class="circle circle_l">
                  <img :src="userAvatar" alt="用户头像" class="avatar" />
                </span>
              </div>
              <div class="time_l">{{ item.time }}</div>
            </div>
          </div>
        </div>
        <div class="setproblem">
          <textarea placeholder="请输入您的问题..." class="input-textarea" id="text" v-model="customerText"
            @keyup.enter="sentMsg()"></textarea>
          <el-button @click="toggleMode()" class="buttonmode">
            <span style="vertical-align: 4px;">{{ mode === 'text2Sql' ? '搜索旅游知识' : '与大模型对话' }}</span>
          </el-button>
          <el-button @click="sentMsg()" class="buttonsend">
            <span style="vertical-align: 4px;">发送</span>
          </el-button>
        </div>
      </div>
    </el-container>
  </el-container>
</template>

<script>
import axios from 'axios';
import userAvatar from '@/assets/user.png';
import robotAvatar from '@/assets/robot.png';
import qs from 'qs';
import axiosInstance from '@/utils/axiosInstance';

export default {
  data() {
    return {
      customerText: "",
      info: [
        {
          type: 'leftinfo',
          time: this.getTodayTime(),
          name: "robot",
          content: "您好，欢迎使用智能地理知识问答系统!",
        }
      ],
      timer: null,
      userAvatar: userAvatar,
      robotAvatar: robotAvatar,
      mode: 'text2Sql', // 初始化模式为text2Sql
      generatedSQL: "", // 存储生成的SQL查询
    }
  },
  created() {
    this.showTimer();
  },
  methods: {
    sentMsg() {
      clearTimeout(this.timer)
      this.showTimer()
      let text = this.customerText;
      if (typeof text === 'string') {
        text = text.trim();
      } else {
        text = '';
      }
      if (text != '') {
        var obj = {
          type: 'rightinfo',
          time: this.getTodayTime(),
          content: text,
        }
        this.info.push(obj)
        this.sendToBackend(this.customerText)
        this.customerText = ''
        this.$nextTick(() => {
          var contentHeight = document.getElementById('content')
          contentHeight.scrollTop = contentHeight.scrollHeight
        })
      }
    },
    async sendToBackend(text) {
      try {
        const token = sessionStorage.getItem('token');
        if (!token) {
          console.error("sessionStorage 中未找到 token");
          return;
        }
        const config = {
          timeout: 60000, // 设置超时时间为 10 秒
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            token: token // 使用自定义头 'token'
          }
        };
        const requestdata = qs.stringify({ text: text });

        let response;
        if (this.mode === 'text2Sql') {
          response = await axiosInstance.post('/text2Sql', requestdata, config);
          console.log("发送请求到/text2Sql,返回为：", response.data);
        } else {
          response = await axiosInstance.post('/textNot2Sql', requestdata, config);
          console.log("发送请求到/textNot2Sql,返回为：", response.data);
        }

        if (response.data.code === 200 && response.data.data) {
          // 将返回的数据转为字符串并传递给 appendRobotMsg 方法
          this.appendRobotMsg(JSON.stringify(response.data.data));
          // 如果生成了SQL查询，保存到 generatedSQL
          if (response.data.sql_query) {
            this.generatedSQL = response.data.sql_query;
          }
        } else {
          this.appendRobotMsg("抱歉，我现在无法回答您的问题。");
        }
      } catch (error) {
        console.error("Error sending message to backend:", error);
        this.appendRobotMsg("抱歉，我现在无法回答您的问题。");
      }
    },
    downloadTable(content) {
      // 查找当前消息对象，获取CSV内容
      const message = this.info.find(item => item.content.includes(content));
      if (!message || !message.csvContent) {
        console.error("未找到对应的CSV内容");
        return;
      }

      // 获取CSV内容
      const csvContent = message.csvContent;

      // 创建一个隐藏的<a>元素
      const link = document.createElement('a');
      link.style.display = 'none';
      document.body.appendChild(link);

      // 设置下载链接的属性
      link.href = 'data:text/csv;charset=utf-8,' + encodeURIComponent(csvContent);
      link.download = 'table.csv';

      // 触发点击事件以开始下载
      link.click();

      // 清理创建的元素
      document.body.removeChild(link);
    },


    appendRobotMsg(text) {
      // 清除定时器并重新设置
      clearTimeout(this.timer);
      this.showTimer();

      // 处理返回的数据
      let answerText;
      let csvContent = '';

      if (typeof text === 'string') {
        text = text.trim();
        try {
          const data = JSON.parse(text);
          if (Array.isArray(data)) {
            // 创建表格
            answerText = '<table border="1">';
            // 添加表头
            answerText += '<tr>';
            const headers = Object.keys(data[0]);
            headers.forEach(header => {
              answerText += `<th>${header}</th>`;
              csvContent += `${header},`;
            });
            csvContent = csvContent.slice(0, -1); // 移除最后一个逗号
            csvContent += '\n';
            answerText += '</tr>';

            // 添加数据行
            data.forEach(item => {
              answerText += '<tr>';
              headers.forEach(header => {
                answerText += `<td>${item[header]}</td>`;
                csvContent += `${item[header]},`;
              });
              csvContent = csvContent.slice(0, -1); // 移除最后一个逗号
              csvContent += '\n';
              answerText += '</tr>';
            });
            answerText += '</table>';
          } else {
            answerText = text;
          }
        } catch (e) {
          answerText = text;
        }
      } else {
        answerText = '抱歉，我现在无法回答您的问题。';
      }

      // 添加到对话框中显示
      let obj = {
        type: "leftinfo",
        time: this.getTodayTime(),
        name: "robot",
        content: answerText,
        question: [],
        // 添加 SQL 查询结果
        sql: this.generatedSQL,
        csvContent: csvContent, // 将生成的CSV内容添加到对象中
        mode: this.mode // 记录当前模式
      };
      this.info.push(obj);
      this.generatedSQL = ""; // 重置 generatedSQL

      // 滚动到底部
      this.$nextTick(() => {
        var contentHeight = document.getElementById('content');
        contentHeight.scrollTop = contentHeight.scrollHeight;
      });
    },


    sentMsgById(val, id) {
      clearTimeout(this.timer)
      this.showTimer()
      let robotById = this.robotAnswer.filter((item) => {
        return item
      });
      let obj_l = {
        type: 'leftinfo',
        time: this.getTodayTime(),
        name: 'robot',
        content: robotById[0].content,
        question: [],
      };
      let obj_r = {
        type: 'rightinfo',
        time: this.getTodayTime(),
        name: 'robot',
        content: val,
        question: [],
      };
      this.info.push(obj_r)
      this.info.push(obj_l)
      this.$nextTick(() => {
        var contentHeight = document.getElementById('content')
        contentHeight.scrollTop = contentHeight.scrollHeight
      })
    },
    clickRobot(val, id) {
      this.sentMsgById(val, id)
    },
    endMsg() {
      let happyEnding = {
        type: 'leftinfo',
        time: this.getTodayTime(),
        content: "退出",
        question: [],
      };
      this.info.push(happyEnding)
      this.$nextTick(() => {
        var contentHeight = document.getElementById('content')
        contentHeight.scrollTop = contentHeight.scrollHeight
      })
    },
    showTimer() {
      this.timer = setTimeout(this.endMsg, 1000 * 60)
    },
    getTodayTime() {
      var day = new Date()
      let seconds = day.getSeconds()
      if (seconds < 10) {
        seconds = "0" + seconds
      }
      var time = day.getHours() + ":" + day.getMinutes() + ":" + seconds
      return time
    },
    goToWeather() {
      this.$router.push({ path: "/weather" });
    },
    goToDataCenter() {
      this.$router.push({ path: "/DataCenter" });
    },
    logout() {
      sessionStorage.removeItem('token');
      this.$router.push({ path: "/login" });
    },
    toggleMode() {
      this.mode = this.mode === 'text2Sql' ? 'textNot2Sql' : 'text2Sql';
    }
  }
}
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

#content {
  height: 480px;
  overflow-y: scroll;
  font-size: 14px;
  width: 100%;
}

.circle {
  display: inline-block;
  width: 34px;
  height: 34px;
  border-radius: 50%;
  background-color: #eff1f3;
}

.con_text {
  color: #333;
  margin-bottom: 5px;
}

.con_que {
  color: #1c88ff;
  height: 30px;
  line-height: 30px;
  cursor: pointer;
}

.info_r {
  position: relative;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
}

.circle_r,
.circle_l {
  display: inline-block;
  vertical-align: top;
}

.circle_r .avatar,
.circle_l .avatar {
  display: block;
}

.circle_r {
  position: absolute;
  left: 0%;
}

.pic_r {
  width: 17px;
  height: 17px;
  margin: 8px;
}

.con_r {
  display: inline-block;
  width: 55%;
  min-height: 55px;
  background-color: #e2e2e2;
  border-radius: 6px;
  padding: 10px;
  margin-left: 40px;
}

.time_r {
  margin-left: 45px;
  color: #999999;
  font-size: 12px;
}

.info_l {
  text-align: right;
  color: #ffffff;
  color: #3163C5;
  margin-top: 10px;
}

.pic_l {
  width: 13px;
  height: 17px;
  margin: 8px 10px;
}

.time_l {
  margin-right: 45px;
  color: #999999;
  font-size: 12px;
  margin-top: 5px;
}

.con_l {
  display: inline-block;
  width: 220px;
  min-height: 51px;
  background-color: #3163C5;
  border-radius: 6px;
  padding: 10px;
  text-align: left;
  color: #fff;
  margin-right: 5px;
}

.setproblem {
  width: 90%;
  height: 68px;
  background-color: #ffffff;
  position: relative;
  margin-top: 20px;
  padding-bottom: 20px;
  display: flex;
  align-items: center;
}

.input-textarea {
  height: 68px;
  width: calc(100% - 150px);
  resize: none;
  padding-right: 10px;
  outline: none;
  border-color: #ccc;
  border-radius: 5px;
  margin-right: 10px;
}

.buttonsend,
.buttonmode {
  width: 120px;
  background: #3163C5;
  opacity: 1;
  border-radius: 4px;
  color: #ffffff;
  cursor: pointer;
  border: none;
}

.buttonsend {
  margin-left: 10px;
}

.buttonmode {
  right: 5px;
  top: 10%;
}

.czkj-item-title {
  line-height: 25px;
  border-bottom: 1px solid #ccc;
  padding-bottom: 5px;
  margin-bottom: 5px;
}

.czkj-item-question {
  cursor: pointer;
  display: block;
  padding: 8px;
  position: relative;
  border-bottom: 1px dashed #ccc;
  line-height: 20px;
  min-height: 20px;
  overflow: hidden;
}

.czkj-question-msg {
  float: left;
  font-size: 14px;
  color: #3163C5;
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
}

.home-container {
  height: 100%;
}

.el-aside {
  background-color: #545c64;
  height: 92.8vh;
}

.sql-output {
  margin-top: 10px;
  padding: 10px;
  background-color: #f0f0f0;
  border-radius: 5px;
}

.sql-output h3 {
  margin-bottom: 5px;
}
</style>
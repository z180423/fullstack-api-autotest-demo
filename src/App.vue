<template>
  <div style="padding: 50px; font-family: sans-serif;">
    <h2>前端测试页面</h2>
    
    <div style="margin-bottom: 15px;">
      <label>用户名：</label>
      <input v-model="username" placeholder="请输入用户名" />
    </div>
    
    <div style="margin-bottom: 15px;">
      <label>密&nbsp;&nbsp;&nbsp;码：</label>
      <input v-model="password" type="password" placeholder="请输入密码" />
    </div>

    <button @click="handleRegister" style="padding: 8px 15px; cursor: pointer;">
      测试注册接口
    </button>

    <p style="color: green; font-weight: bold; margin-top: 20px;">
      {{ message }}
    </p>
  </div>
</template>

<script setup>
import { ref } from 'vue'

// 定义响应式变量，用来绑定输入框和显示结果
const username = ref('')
const password = ref('')
const message = ref('')

// 点击按钮时执行的函数
const handleRegister = async () => {
  if (!username.value || !password.value) {
    message.value = '用户名和密码不能为空！'
    return
  }

  try {
    // 请求你服务器上的接口
    const response = await fetch('http://123.56.96.199/api/register', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        username: username.value,
        password: password.value
      })
    })
    
    const data = await response.json()
    message.value = `后端返回：${data.msg}`

  } catch (error) {
    // 如果报错，大概率是跨域问题或者后端没开
    console.error(error)
    message.value = '请求失败，请按 F12 查看控制台报错'
  }
}
</script>

<style>
/* 这里暂时不需要写额外的样式，我们把样式直接写在了标签里 */
</style>
## Multi-user task management system

This is project is a multi-user task manage system based on socket communication. We designed communication protocol and used socket programming for implementation. Users can manager their lives by adding, updating and archiving task cards with an attractive GUI using Kivy.

![](https://gitee.com/hzy46/kivy-task-manager/raw/master/images/show.png)

## Basic Functions

### 1. Add a task

To add a task, one can click the ![输入图片说明](https://images.gitee.com/uploads/images/2018/1205/145028_a0359296_725860.png "button0.png") button at the upper-right corner, then fill in all the needed information. The task title is required, while the expecting date, color tag and detailed information are optional.

![](https://gitee.com/hzy46/kivy-task-manager/raw/master/images/im1.png)

### 2. Change the status of a task

There are three default lists to classify tasks in different statuses. One can drag the task card to the expected list. This will change the status of a task.

![](https://gitee.com/hzy46/kivy-task-manager/raw/master/images/im2.png)

### 3. The network log panel

There is a network log panel which shows the network communication details. One can click the ![](https://gitee.com/hzy46/kivy-task-manager/raw/master/images/button.png) button at the upper-right corner. Since we wanted to design a communication protocol, this log panel is very useful when debugging.

![](https://gitee.com/hzy46/kivy-task-manager/raw/master/images/im3.png)

![](https://gitee.com/hzy46/kivy-task-manager/raw/master/images/im4.png)

### 4. Change the theme

One can change themes by clicking the ![](https://gitee.com/hzy46/kivy-task-manager/raw/master/images/button2.png) button at the upper-right corner. There are 6 predefined themes. The change of themes can be stored to the server and the settings will be loaded when users log in the next time.

![](https://gitee.com/hzy46/kivy-task-manager/raw/master/images/im6.png)



## Quick Start

Please install Python and Kivy first. Then start the backend with:

```
python server.py
```

To start the application, please run:

```
kivy main.py
```


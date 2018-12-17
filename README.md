
# IT项目大作业 - *MuteX*


## Version 1.0
 - 2018.12.17 12:00
<br>

## Version 1.5
 - 2018.12.17 17:30
 - 修复大量bug

<br>

### 目录结构说明

- `ServerFacade.py` 是项目服务器端的启动文件
<br>

- `/client` 存放前端的源文件和模板文件
    - `/static` 存放静态文件,CSS,JS,图片等
    - `index.html` HTML文件
<br>

- `/server` 是存放服务器端所有代码的主要文件
    - `/data`
        - `DBcontext.py` 与数据库交互的上下文管理器源码
    - `/DBmanagement`
        - `UserDBmanagement.py`
        - `BookDBmanagement.py`
        - `OrderDBmanagement.py`
        - `PublishDBmanagement.py`
        - `AdminDBmanagement.py`
    - `/management`
        - `UserManagement.py`
        - `BookManagement.py`
        - `OrderManagement.py`
        - `PublishManagement.py`
        - `AdminManagement.py`
    - `/mutex` 存放可能使用到的,耦合度较高的模块,存放到一起做工具集
<br>

- `/database` 存放数据库元文件和其他配置文件
  - `mutex.db`  数据库文件
  - `/Files`  存放图片实体文件
<br>

- `/doc` 这个文件夹是放开发时需要的文档的
  - `state.md` 状态码文档，是前端对响应做出判断需要的文档
  - `mutex.port` 接口文档，是一个约束前后端交互的文档
<br>

- `requirement.txt` 后端python需要安装的库, 后续可能会添加

<br>

#### 项目搭建前

> &emsp;
> //安装所需的库
> pip install -r requirement.txt
> &emsp;

<br/>

#### 注意
1. 状态码文档，大家可以随便加数值，**不重复**即可，但是**不是自己添加的内容**，
   **绝对不可以随便删改**。
2. `.port`文件是我随便起的扩展名，内容格式也比较随意，但都能看得懂。

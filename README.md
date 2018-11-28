
# IT项目大作业


### 目录结构说明

- `run.py` 是项目服务器端的启动文件

- `/client` 存放前端的源文件和模板文件
    - `/static` 存放静态文件,CSS,JS,图片等
    - `/template` 存放编写好的HTML模板文件

- `/server` 是存放服务器端所有代码的主要文件
    - `/data`
        - `/database` 存放数据库元文件和其他配置文件
        - `DBcontext.py` 与数据库交互的上下文管理器源码
    - `/DBmanagement`
        - `UserDBmanagement.py`
        - `BookDBmanagement.py`
        - `OrderDBmanagement.py`
        - `PublishDBmanagement.py`
    - `/management`
        - `UserManagement.py`
        - `BookManagement.py`
        - `OrderManagement.py`
        - `PublishManagement.py`
    - `/mutex` 存放可能使用到的,耦合度较高的模块,存放到一起做工具集
    - `ServerFacade.py` 服务器调度模块

- `requirement.txt` 后端python需要安装的库, 后续可能会添加


#### 项目搭建前

> &emsp;
> pip install -r requirement.txt
> &emsp;


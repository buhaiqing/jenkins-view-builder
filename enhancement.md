## 改进点
- 提供Python2支持，去除对cmd2依赖(只能用于Python3.5以上的版本)
- view 支持中文名(源库只支持Python3，代码上对同时支持Python2/Python str的代码不规范)
- 使用python-jenkins库，解决CSRF protection问题


## 常见问题
### 中文名支持
- view 中含有中文 -   *已支持*
- job 中含有中文  -  *支持*

### no valid crumb was included in the request解决
- https://www.zhyea.com/2016/10/14/resolve-no-valid-crumb-was-included-in-the-request-error.html
- https://thepracticalsysadmin.com/fix-the-jenkinsapi-no-valid-crumb-error/

[CSRF Security](https://wiki.jenkins.io/display/JENKINS/Remote+access+API#RemoteaccessAPI-CSRFProtection)

### folder
如存在folder 直接使用根目录, 如folder1/job1 ，在job定义时候使用folder1即可

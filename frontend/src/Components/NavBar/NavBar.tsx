import { DashboardOutlined, DatabaseOutlined, LogoutOutlined, SecurityScanOutlined, UserOutlined } from '@ant-design/icons';
import { Menu } from 'antd';
import React, { ReactElement } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../../Hooks/AuthContextProvider';

const { SubMenu } = Menu;

export const NavBar = (): ReactElement => {
  const location = useLocation();
  const auth = useAuth();

  return (
    <Menu
      theme='dark'
      selectedKeys={[location.pathname]}
      mode='inline'
    >
      <Menu.Item
        key='/'
        icon={<DashboardOutlined />}
      >
        <Link to='/'>Dashboard</Link>
      </Menu.Item>
      <SubMenu
        key='users'
        icon={<UserOutlined />}
        title='Users'
      >
        <Menu.Item key='users:users'>Users</Menu.Item>
        <Menu.Item key='users:organizations'>Organizations</Menu.Item>
        <Menu.Item key='users:publish-requests'>Publish requests</Menu.Item>
      </SubMenu>
      <SubMenu
        key='registry'
        icon={<DatabaseOutlined />}
        title='Registry'
      >
        <Menu.Item key='/registry/services/wms'><Link to='/registry/services/wms'>WMS</Link></Menu.Item>
        <Menu.Item key='registry:wfs'>WFS</Menu.Item>
        <Menu.Item key='registry:csw'>CSW</Menu.Item>
        <Menu.Item key='/registry/services/layers'><Link to='/registry/services/layers'>Layers</Link></Menu.Item>
        <Menu.Item key='registry:featuretypes'>Feature Types</Menu.Item>
        <Menu.Item key='registry:metadata'>Metadata Records</Menu.Item>
        <Menu.Item key='registry:map-contexts'><Link to='/registry/mapcontexts'>Map Contexts</Link></Menu.Item>
      </SubMenu>
      <SubMenu
        key='security'
        icon={<SecurityScanOutlined />}
        title='Security'
      >
        <Menu.Item key='security:external-auth'>External Authentications</Menu.Item>
        <Menu.Item key='security:service-proxy-settings'>Service proxy settings</Menu.Item>
        <Menu.Item key='security:service-access-groups'>Service Access Groups</Menu.Item>
        <Menu.Item key='security:allowed-operations'>Allowed Operations</Menu.Item>
        <Menu.Item key='scurity:logs'>Logs</Menu.Item>
      </SubMenu>
      <Menu.Item
        key='logout'
        icon={<LogoutOutlined />}
      >
        <Link to='/logout'>Logout ({auth.user})</Link>
      </Menu.Item>
    </Menu>
    //       <AuthButton username={username} handleAuth={handleAuth}/>
    // <Tag color="default">{username}</Tag>
  );
};

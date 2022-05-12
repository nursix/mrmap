import type { RessourceDetailsProps } from '@/components/RessourceDetails';
import RessourceDetails from '@/components/RessourceDetails';
import SchemaForm from '@/components/SchemaForm';
import SchemaTable from '@/components/SchemaTable';
import type { JsonApiDocument, JsonApiPrimaryData } from '@/utils/jsonapi';
import { getIncludesByType } from '@/utils/jsonapi';
import { CheckOutlined, CloseOutlined, EditFilled, LinkOutlined, SearchOutlined } from '@ant-design/icons';
import { Badge, Button, Col, Drawer, Row, Select, Space, Switch, Tooltip, Tree } from 'antd';
import type { DefaultOptionType } from 'antd/lib/select';
import type { Key } from 'rc-tree/lib/interface';
import type { ReactElement, ReactNode } from 'react';
import { useCallback, useState } from 'react';
import { useIntl } from 'umi';


interface Node {
    key: any;
    raw: JsonApiPrimaryData;
    title: string;
    children?: Node[] | undefined;
    rawDescendants?: JsonApiPrimaryData[] | undefined;
    isLeaf: boolean
}

interface NodeOptionType extends DefaultOptionType {
    label: string;
}

export interface OgcServiceDetailsProps extends RessourceDetailsProps {
    loading?: boolean;
    onActiveSwitchChange?: (checked: boolean, ressource: JsonApiPrimaryData) => void;
    nodeRessourceType: string;
}

const getDescendants = (nodes: JsonApiPrimaryData[], currentNode: JsonApiPrimaryData) => {
    return nodes?.filter(
        (node: JsonApiPrimaryData) => node?.attributes?.lft > currentNode?.attributes?.lft && node?.attributes?.rght < currentNode?.attributes?.rght
    );
};

const getChildren = (nodes: JsonApiPrimaryData[], currentNode: JsonApiPrimaryData) => {
    return getDescendants(nodes, currentNode).filter(
        (node: JsonApiPrimaryData) => node?.attributes?.level === currentNode?.attributes.level + 1
    );
};

const mapTreeData = (nodes: JsonApiPrimaryData[], currentNode: JsonApiPrimaryData): Node => {
    const children = getChildren(nodes, currentNode);
    if (children.length === 0){
        return {
            key: currentNode.id, 
            title: currentNode.attributes.stringRepresentation, 
            raw: currentNode,
            isLeaf: true,
        }
    } else {
        const childNodes: Node[] = [];
        children.forEach((child: JsonApiPrimaryData) => {
            childNodes.push(
                mapTreeData(nodes, child)
            );
        });
        return {
            key: currentNode.id, 
            title: currentNode.attributes.stringRepresentation, 
            raw: currentNode,
            isLeaf: false,
            children: childNodes,
            rawDescendants: getDescendants(nodes, currentNode)
        }
    }
};


const transformTreeData = (wms: JsonApiDocument): Node[] => {
    const treeOrderedLayers = 
        getIncludesByType(wms, 'Layer')
        .sort((a: JsonApiPrimaryData, b: JsonApiPrimaryData) => a.attributes.lft - b.attributes.lft);
    const rootNode = treeOrderedLayers[0];
    const children = getDescendants(treeOrderedLayers, rootNode);
    return [mapTreeData(children, rootNode)];
};

const OgcServiceDetails = (
    {
        loading=false,
        onActiveSwitchChange = undefined,
        nodeRessourceType,
        ...passThroughProps
    }: OgcServiceDetailsProps
): ReactElement => {
    /**
     * page hooks
     */
    const intl = useIntl();
    const [ treeData, setTreeData ] = useState<Node[]>();
    const [ flatNodeList, setFlatNodeList ] = useState<JsonApiPrimaryData[]>();
    const [ expandedKeys, setExpandedKeys ] = useState<Key[]>();
    const [ autoExpandParent, setAutoExpandParent ] = useState<boolean>();
    const [ searchOptions, setSearchOptions ] = useState<DefaultOptionType[]>([]);
    const [ selectedSearchKey, setSelectedSearchKey ] = useState<string>();

    const [ selectedForEdit, setSelectedForEdit ] = useState<JsonApiPrimaryData>();
    const [ rightDrawerVisible, setRightDrawerVisible ] = useState<boolean>(false);
    const [ selectedForDataset, setSelectedForDataset ] = useState<JsonApiPrimaryData>();
    
    
    const [ bottomDrawerVisible, setBottomDrawerVisible ] = useState<boolean>(false);

    const [ reFetchRessource, setRefetchRessource ] = useState<boolean>(false);


    const isLoading = loading || passThroughProps.rebuild;


    /**
    * @description Generate extra ui components like edit button for given json:api resource
    */
    const genExtra = useCallback((resource: JsonApiPrimaryData): ReactNode => {
        if (!resource){
            return <></>
        }
        const isActive = resource?.attributes?.isActive;
        const datasetMetadataCount = resource?.relationships?.datasetMetadata?.meta?.count;
        const datasetMetadataButton = (
            <Badge 
                count={datasetMetadataCount}
                size={'small'}>
                <Button
                    size='small'
                    icon={<LinkOutlined />}
                    loading={isLoading}
                    onClick={(event) => {
                        event.stopPropagation();
                        setSelectedForDataset(resource);
                        setBottomDrawerVisible(true);
                    }}
                />
            </Badge>
        );
        return (
            <Space size="small" key={`space-${resource.id}`}>
                {datasetMetadataCount > 0 ? datasetMetadataButton: <></>}
                <Tooltip
                title={
                    isActive
                    ? 'deactivate'
                    : 'activate'
                }
                >
                    <Switch
                        checkedChildren={<CheckOutlined />}
                        unCheckedChildren={<CloseOutlined />}
                        defaultChecked={isActive}
                        checked={isActive}
                        onClick={
                            (checked, event) => {
                                // If you don't want click extra trigger collapse, you can prevent this:
                                event.stopPropagation();
                                if (onActiveSwitchChange){
                                    onActiveSwitchChange(checked, resource);
                                }
                            }
                        }
                        loading={isLoading}
                        key={`activate-switch-${resource.id}`}
                    />
                </Tooltip>
                <Tooltip
                title='edit metadata'
                >
                    <Button
                        size='small'
                        icon={<EditFilled />}
                        style={{ borderColor: 'gold', color: 'gold' }}
                        onClick={
                            (event) => {
                                event.stopPropagation();
                                setRightDrawerVisible(true);
                                setSelectedForEdit(resource);
                            }
                        }
                        loading={isLoading}
                        key={`edit-btn-${resource.id}`}
                    />
                </Tooltip>
            </Space>
        );
    }, [isLoading]);
           
    const search = useCallback((key) => {
        const keys = flatNodeList?.filter((node) => node?.id === key).map(node => node.id);
        setExpandedKeys(keys);
        setAutoExpandParent(true);
        setSelectedSearchKey(key);
    }, [flatNodeList]);

    const onExpand = useCallback((keys: Key[]) => {
        setExpandedKeys(keys);
        setAutoExpandParent(false);
    }, []);

    const getNodeTitle = useCallback((node: Node) => {
        const title = selectedSearchKey && node.key === selectedSearchKey ? (
            <span>
              <SearchOutlined style={{color: '#f50'}} />
              <span style={{color: '#f50'}}>{node.title}</span>
            </span>
          ) : (
            <span>{node.title}</span>
          );
        return (
            <Row justify='space-between' style={{width: '100%'}}>
                <Col span={8}>
                    {title}
                </Col>
                 <Col span={8}>
                    {genExtra(node.raw)}
                 </Col>
                
            </Row>
        )
    },[genExtra, selectedSearchKey]);

    const onRessourceResponse = useCallback((ressource: JsonApiDocument) => {        
        setRefetchRessource(false);
        setTreeData(transformTreeData(ressource));

        const newSearchOptions: DefaultOptionType[] = getIncludesByType(ressource, nodeRessourceType).map((node: JsonApiPrimaryData) => {
            return {
                value: node.id,
                label: node.attributes.stringRepresentation
            }
        })
        setSearchOptions(newSearchOptions);
    }, [nodeRessourceType]);

    // useEffect(() => {
    //     setRefetchRessource(true);
    // }, [updateLayerResponse, updateWmsResponse]);

    return (
        <RessourceDetails
            {...passThroughProps}
            //resourceType={passThroughProps.resourceType}
            //additionalGetRessourceParams={getWebMapServiceParams}
            //onRessourceResponse={onRessourceResponse}
            //rebuild={reFetchRessource}
            rebuild={reFetchRessource}
            
        > 
            <Select 
                style={{ marginBottom: 8, width: '100%' }} 
                showSearch={true}
                allowClear={true}
                onSelect={search}
                onDeselect={() => {setSelectedSearchKey(undefined)}}
                options={searchOptions}
                dropdownMatchSelectWidth={false}
                placeholder={
                    intl.formatMessage(
                        { id: 'pages.wmsDetail.searchLayer' }
                    )
                }
                optionFilterProp="label"
                filterOption={
                    (input, option) => {
                        return option?.label?.toLocaleLowerCase().includes(input.toLocaleLowerCase()) ? true: false;
                    }
                }
                key={'layer-search-select'}
            />
            <Tree
                showLine={true}
                expandedKeys={expandedKeys}
                onExpand={onExpand}
                autoExpandParent={autoExpandParent}
                titleRender={getNodeTitle}
                treeData={treeData}
            />
             
            <Drawer
                title={
                    intl.formatMessage(
                        { id: 'pages.wmsDetail.editRessource' },
                        { type: selectedForEdit?.type, label: selectedForEdit?.attributes.stringRepresentation },
                    )
                }
                placement="right"
                visible={rightDrawerVisible}
                onClose={() => { setRightDrawerVisible(false);}}
                destroyOnClose={true}
            >
                <SchemaForm
                    resourceType={selectedForEdit?.type || 'Layer'}
                    resourceId={selectedForEdit?.id}
                    onSuccess={() => {
                        setRightDrawerVisible(false);
                    }}
                />
            </Drawer>
            <Drawer
                title={
                    intl.formatMessage(
                        { id: 'pages.wmsDetail.linkedDatasetMetadata' },
                        { type: selectedForDataset?.type, label: selectedForDataset?.attributes.stringRepresentation },
                    )
                }
                placement="bottom"
                visible={bottomDrawerVisible}
                onClose={() => {setBottomDrawerVisible(false);}}
                destroyOnClose={true}
                size={'large'}
            >
                <SchemaTable
                    resourceTypes={{baseResourceType: "DatasetMetadata", nestedResource: selectedForDataset ? {type: selectedForDataset?.type, id: selectedForDataset?.id}: undefined }}
                />
            </Drawer>
        </RessourceDetails>
    );
};

export default OgcServiceDetails;


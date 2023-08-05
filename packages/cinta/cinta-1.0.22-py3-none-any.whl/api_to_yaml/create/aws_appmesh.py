#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import boto3

class AppMeshController:
    """
    Controller for VirtualRouter
    """

    def __init__(self):
        self._appmesh = boto3.client('appmesh')

    
    def create_virtual_router(self, *args, **kwargs):
        """
        Create a VirtualRouter
        """
        mesh_name = kwargs.get('meshName')
        virtual_router_name = kwargs.get('virtualRouterName')
        spec = kwargs.get('spec')
        
        routes = spec.pop('routes')

        resp = self._appmesh.create_virtual_router(
            meshName=mesh_name,
            virtualRouterName=virtual_router_name,
            spec=spec,
            tags=kwargs.get('tags')
        )

        for route in routes:
            self._appmesh.create_route(
                meshName=mesh_name,
                virtualRouterName=virtual_router_name,
                routeName=route.pop('name'),
                spec=route,
                tags=kwargs.get('tags')
            )

        return resp

    def update_virtual_router(self, *args, **kwargs):
        """
        Update a VirtualRouter
        """
        mesh_name = kwargs.get('meshName')
        virtual_router_name = kwargs.get('virtualRouterName')
        spec = kwargs.get('spec')

        route_map = {route.pop("name"): route for route in spec.pop('routes')}
        
        old_routes = set()
        for route in self._appmesh.list_routes(
            limit=100,
            meshName=mesh_name,
            virtualRouterName=virtual_router_name
        )['routes']:
            if route['routeName'] not in route_map:
                self._appmesh.delete_route(
                    meshName=mesh_name,
                    virtualRouterName=virtual_router_name,
                    routeName=route['routeName']
                )
            else:
                old_routes.add(route['routeName'])
                
        for name, route in route_map.items():
            if name in old_routes:
                self._appmesh.update_route(
                    meshName=mesh_name,
                    virtualRouterName=virtual_router_name,
                    routeName=name,
                    spec=route
                )
            else:
                self._appmesh.create_route(
                    meshName=mesh_name,
                    virtualRouterName=virtual_router_name,
                    routeName=name,
                    spec=route
                )
        
        return self._appmesh.update_virtual_router(
            meshName=mesh_name,
            virtualRouterName=virtual_router_name,
            spec=spec
        )

    def delete_virtual_router(self, *args, **kwargs):
        """
        Delete a VirtualRouter
        """
        mesh_name = kwargs.get('meshName')
        virtual_router_name = kwargs.get('virtualRouterName')

        for route in self._appmesh.list_routes(
            limit=100,
            meshName=mesh_name,
            virtualRouterName=virtual_router_name
        )['routes']:
            self._appmesh.delete_route(
                meshName=mesh_name,
                virtualRouterName=virtual_router_name,
                routeName=route['routeName']
            )
        
        return self._appmesh.delete_virtual_router(
            meshName=mesh_name,
            virtualRouterName=virtual_router_name
        )

    def create_virtual_gateway(self, *args, **kwargs):
        """
        Create a VirtualGateway
        """
        mesh_name = kwargs.get('meshName')
        virtual_gateway_name = kwargs.get('virtualGatewayName')
        spec = kwargs.get('spec')
        routes = spec.pop('routes')

        resp = self._appmesh.create_virtual_gateway(
            meshName=mesh_name,
            virtualGatewayName=virtual_gateway_name,
            spec=spec,
            tags=kwargs.get('tags')
        )

        for route in routes:
            self._appmesh.create_gateway_route(
                meshName=mesh_name,
                virtualGatewayName=virtual_gateway_name,
                gatewayRouteName=route.pop('name'),
                spec=route,
                tags=kwargs.get('tags')
            )

        return resp

    def update_virtual_gateway(self, *args, **kwargs):
        """
        Update a VirtualGateway
        """
        mesh_name = kwargs.get('meshName')
        virtual_gateway_name = kwargs.get('virtualGatewayName')
        spec = kwargs.get('spec')

        route_map = {route.pop("name"): route for route in spec.pop('routes')}
        
        old_routes = set()
        for route in self._appmesh.list_gateway_routes(
            limit=100,
            meshName=mesh_name,
            virtualGatewayName=virtual_gateway_name
        )['gatewayRoutes']:
            if route['gatewayRouteName'] not in route_map:
                self._appmesh.delete_gateway_route(
                    meshName=mesh_name,
                    virtualGatewayName=virtual_gateway_name,
                    gatewayRouteName=route['gatewayRouteName']
                )
            else:
                old_routes.add(route['gatewayRouteName'])
                
        for name, route in route_map.items():
            if name in old_routes:
                self._appmesh.update_gateway_route(
                    meshName=mesh_name,
                    virtualGatewayName=virtual_gateway_name,
                    gatewayRouteName=name,
                    spec=route
                )
            else:
                self._appmesh.create_gateway_route(
                    meshName=mesh_name,
                    virtualGatewayName=virtual_gateway_name,
                    gatewayRouteName=name,
                    spec=route
                )
        
        return self._appmesh.update_virtual_gateway(
            meshName=mesh_name,
            virtualGatewayName=virtual_gateway_name,
            spec=spec
        )

    def delete_virtual_router(self, *args, **kwargs):
        """
        Delete a VirtualGateway
        """
        mesh_name = kwargs.get('meshName')
        virtual_gateway_name = kwargs.get('virtualGatewayName')

        for route in self._appmesh.list_gateway_routes(
            limit=100,
            meshName=mesh_name,
            virtualGatewayName=virtual_gateway_name
        )['gatewayRoutes']:
            self._appmesh.delete_route(
                meshName=mesh_name,
                virtualGatewayName=virtual_gateway_name,
                gatewayRouteName=route['gatewayRouteName']
            )
        
        return self._appmesh.delete_virtual_gateway(
            meshName=mesh_name,
            virtualGatewayName=virtual_gateway_name
        )

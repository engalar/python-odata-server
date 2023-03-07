import werkzeug
from flask import Flask

from odata_server.flask import odata_bp
import pymongo

# docker run -itd --name mongo -p 27017:27017 mongo
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mongo = myclient["runoobdb"]

edmx = {
    "DataServices": [
        {

            "Namespace": "DefaultNamespace",
            "EntityTypes": [
                {
                         "Name": "Entity",
                         "Key": [{"Name": "Attribute"}],
                         "Properties": [
                             {"Nullable": False, "Name": "Attribute", "Type": "Edm.String", "MaxLength": "200"},
                         ],
                },
            ],
            "EntityContainers": [
                {
                    "Name": "Entities",
                    "EntitySets": [
                        {
                            "Name": "Entitys",
                            "EntityType": "DefaultNamespace.Entity",
                            "Annotations": [
                                {
                                    "Term": "Org.OData.Capabilities.V1.InsertRestrictions",
                                    "Record": {
                                        "PropertyValues": [
                                            {
                                                "Property": "Insertable",
                                                "Bool": "true"
                                            },
                                            {
                                                "Property": "MaxLevels",
                                                "Int": "0"
                                            }, {
                                                "Property": "TypecastSegmentSupported",
                                                "Bool": "false"
                                            },
                                        ]
                                    }
                                }, {
                                    "Term": "Org.OData.Capabilities.V1.DeepInsertSupport",
                                    "Record": {
                                        "PropertyValues": [
                                            {
                                                "Property": "Supported",
                                                "Bool": "false"
                                            },
                                            {
                                                "Property": "ContentIDSupported",
                                                "Bool": "false"
                                            },
                                        ]
                                    }
                                },
                                {
                                    "Term": "Org.OData.Capabilities.V1.UpdateRestrictions",
                                    "Record": {
                                        "PropertyValues": [
                                            {
                                                "Property": "Updatable",
                                                "Bool": "true"
                                            }, {
                                                "Property": "DeltaUpdateSupported",
                                                "Bool": "true"
                                            }, {
                                                "Property": "UpdateMethod",
                                                "EnumMember": "Org.OData.Capabilities.V1.HttpMethod/PATCH"
                                            }, {
                                                "Property": "FilterSegmentSupported",
                                                "Bool": "false"
                                            }, {
                                                "Property": "TypecastSegmentSupported",
                                                "Bool": "false"
                                            }, {
                                                "Property": "NonUpdatableProperties",
                                                "Collection": {
                                                    "Items": [{"PropertyPath": "Attribute"}]
                                                }
                                            }, {
                                                "Property": "MaxLevels",
                                                "Int": "0"
                                            }
                                        ]
                                    }
                                }, {
                                    "Term": "Org.OData.Capabilities.V1.DeleteRestrictions",
                                    "Record": {
                                        "PropertyValues": [
                                            {"Property": "Deletable", "Bool": "true"},
                                            {"Property": "MaxLevels", "Int": "0"},
                                            {"Property": "FilterSegmentSupported", "Bool": "false"},
                                            {"Property": "TypecastSegmentSupported", "Bool": "false"},
                                        ]
                                    }
                                }, {
                                    "Term": "Org.OData.Capabilities.V1.FilterRestrictions",
                                    "Record": {
                                        "PropertyValues": [
                                            {"Property": "Filterable", "Bool": "true"},
                                        ]
                                    }
                                }, {
                                    "Term": "Org.OData.Capabilities.V1.SortRestrictions",
                                    "Record": {
                                        "PropertyValues": [
                                            {"Property": "Sortable", "Bool": "true"},
                                        ]
                                    }
                                }, {
                                    "Term": "Org.OData.Capabilities.V1.CountRestrictions",
                                    "Record": {
                                        "PropertyValues": [
                                            {"Property": "Countable", "Bool": "true"},
                                        ]
                                    }
                                }, {
                                    "Term": "Org.OData.Capabilities.V1.SearchRestrictions",
                                    "Record": {
                                        "PropertyValues": [
                                            {
                                                "Property": "Searchable",
                                                "Bool": "false"
                                            }
                                        ]
                                    }
                                }
                            ],
                        },
                    ],
                    "Annotations": [
                        {
                            "Term": "Org.OData.Capabilities.V1.BatchSupported",
                            "Bool": "false"
                        },
                        {
                            "Term": "Org.OData.Capabilities.V1.CrossJoinSupported",
                            "Bool": "false"
                        },
                        {
                            "Term": "Org.OData.Capabilities.V1.QuerySegmentSupported",
                            "Bool": "true"
                        },
                        {
                            "Term": "Org.OData.Capabilities.V1.SupportedFormats",
                            "Collection": {
                                "Items": [
                                    {
                                        "String": "application/json"
                                    }
                                ]
                            }
                        }
                    ],
                }
            ],
        },
        {
            "Namespace": "Com.Mendix",
            "Alias": "Mendix",
            "Terms": [{
                "Name": "IsAttribute",
                "Type": "Edm.Boolean",
            }]
        }
    ]
}


app = Flask(__name__)
app.register_blueprint(odata_bp, options={"mongo": mongo, "edmx": edmx}, url_prefix="")

if __name__ == "__main__":
    app.run()

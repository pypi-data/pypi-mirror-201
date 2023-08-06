import unittest
from parameterized import parameterized
from core.types import Finding, FindingType, Severity, RelatedConfig, WellDoneRating, Violation


class FindingTests(unittest.TestCase):
    related_config_1 = RelatedConfig()
    related_config_1.config_id = "bucket.lifecycle_configuration.rules[0].id"
    related_config_1.preferred_value = "VersioningLifecycleManagementRule"
    related_config_1.comment = "change name to a name for your rule"

    related_config_2 = RelatedConfig()
    related_config_2.config_id = "bucket.lifecycle_configuration.rules[0].status"
    related_config_2.preferred_value = "Enabled"

    related_configs = [related_config_1, related_config_2]

    @parameterized.expand(
        [
            [Finding(
                finding_type=FindingType.DesignGap,
                gap="S3 Lifecycle configuration is not defined",
                rating=Severity.Critical,
                desc="Define the appropriate lifecycle configuration",
                config_id='bucket.lifecycle_configuration',
                related_configs=related_configs),
                False,
                'Design Gap Finding w/ Related Configs - No Exceptions'
            ],
            [Finding(
                finding_type=FindingType.ResourceGap,
                gap="Dynamo DB tables are not globally available",
                rating=Severity.High,
                desc="Since your design preference is to have a globally available database, use DynamoDB Global tables instead",
                config_id='db'),
                False,
                'Resource Gap Finding - No Exceptions'
            ],
            [Finding(
                finding_type=FindingType.Kudos,
                config_id='key.algorithm',
                desc="Key algorithm is set to AES-GCM",
                rating=WellDoneRating.Amazing),
                False,
                'Well Done Finding - No Exceptions'
            ],
            [Finding(
                FindingType.Task,
                req_id='Oak9.Req.KM.1',
                desc="Ensure that a breakglass account is created for AWS and follow best practices here"),
                False,
                'Task Finding - No Exceptions'
            ]
        ]
    )
    def test_finding(self, finding: Finding, ex: bool, description: str):
        if ex:
            self.assertIsInstance(finding, Finding, description)
        else:
            self.assertNotIsInstance(finding, Finding, description)

    @parameterized.expand(
        [
            [Violation(
                config_id='a.b.c',
                config_gap='Gap',
                config_fix='fix',
                config_value='9',
                preferred_value='10',
                additional_guidance='additional guidance',
                documentation='https://www.oak9.io',
                adjusted_severity=Severity.Moderate,
                severity=Severity.High
            ),
                'Design Gap Finding w/ Related Configs - No Exceptions'
            ]

        ]
    )
    def test_finding(self, finding: Finding, description: str):
        self.assertIsInstance(finding, Finding, description)

from types import Violation, Capabilities


class ViolationTests(unittest.TestCase):

    def test_eq(self):
        violation_1 = Violation(config_id='foo', capability_id=Capabilities.DATA_ENCRYPTION_AT_REST.id)
        self.assertEqual(violation_1, violation_1)

        violation_2 = Violation(config_id='bar', capability_id=Capabilities.DATA_ENCRYPTION_AT_REST.id)
        self.assertNotEqual(violation_1, violation_2)

    def test_support_set_protocol(self):
        violation_1 = Violation(config_id='foo', capability_id=Capabilities.DATA_ENCRYPTION_AT_REST.id)
        fixture = set()
        fixture.add(violation_1)
        fixture.add(violation_1)
        self.assertTrue(violation_1 in fixture)
        self.assertEqual(1, len(fixture))

        violation_2 = Violation(config_id='bar', capability_id=Capabilities.DATA_ENCRYPTION_AT_REST.id)
        self.assertFalse(violation_2 in fixture)

        fixture.add(violation_2)
        self.assertTrue(violation_1 in fixture)
        self.assertTrue(violation_2 in fixture)
        self.assertEqual(2, len(fixture))

    def test_hashing(self):
        violation_1 = Violation(config_id='foo', capability_id=Capabilities.DATA_ENCRYPTION_AT_REST.id)
        fixture: dict[Violation, int] = dict()
        fixture[violation_1] = 10
        self.assertEqual(10, fixture[violation_1])


if __name__ == '__main__':
    unittest.main()

-- ============================================================================
-- fifa_teams.sql
-- Reference table of the 211 official FIFA member associations for wc2026 DB.
--
-- Names follow the conventions of the common "International football results"
-- dataset (e.g. 'Ivory Coast', 'South Korea', 'United States') so they JOIN
-- cleanly against results.home_team / results.away_team.
--
-- IMPORTANT: names below are unverified against your actual results table
-- (no DB access at build time). Run the VERIFY query at the bottom FIRST and
-- reconcile any mismatches before relying on the filter.
-- ============================================================================

USE wc2026;

DROP TABLE IF EXISTS fifa_teams;

CREATE TABLE fifa_teams (
    team_name      VARCHAR(60)  NOT NULL PRIMARY KEY,
    confederation  ENUM('UEFA','CONMEBOL','CONCACAF','CAF','AFC','OFC') NOT NULL,
    is_wc2026      TINYINT(1)   NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ---------------------------------------------------------------------------
-- UEFA (55)
-- ---------------------------------------------------------------------------
INSERT INTO fifa_teams (team_name, confederation) VALUES
('Albania','UEFA'),('Andorra','UEFA'),('Armenia','UEFA'),('Austria','UEFA'),
('Azerbaijan','UEFA'),('Belarus','UEFA'),('Belgium','UEFA'),
('Bosnia and Herzegovina','UEFA'),('Bulgaria','UEFA'),('Croatia','UEFA'),
('Cyprus','UEFA'),('Czech Republic','UEFA'),('Denmark','UEFA'),('England','UEFA'),
('Estonia','UEFA'),('Faroe Islands','UEFA'),('Finland','UEFA'),('France','UEFA'),
('Georgia','UEFA'),('Germany','UEFA'),('Gibraltar','UEFA'),('Greece','UEFA'),
('Hungary','UEFA'),('Iceland','UEFA'),('Israel','UEFA'),('Italy','UEFA'),
('Kazakhstan','UEFA'),('Kosovo','UEFA'),('Latvia','UEFA'),('Liechtenstein','UEFA'),
('Lithuania','UEFA'),('Luxembourg','UEFA'),('Malta','UEFA'),('Moldova','UEFA'),
('Montenegro','UEFA'),('Netherlands','UEFA'),('North Macedonia','UEFA'),
('Northern Ireland','UEFA'),('Norway','UEFA'),('Poland','UEFA'),('Portugal','UEFA'),
('Republic of Ireland','UEFA'),('Romania','UEFA'),('Russia','UEFA'),
('San Marino','UEFA'),('Scotland','UEFA'),('Serbia','UEFA'),('Slovakia','UEFA'),
('Slovenia','UEFA'),('Spain','UEFA'),('Sweden','UEFA'),('Switzerland','UEFA'),
('Turkey','UEFA'),('Ukraine','UEFA'),('Wales','UEFA');

-- ---------------------------------------------------------------------------
-- CONMEBOL (10)
-- ---------------------------------------------------------------------------
INSERT INTO fifa_teams (team_name, confederation) VALUES
('Argentina','CONMEBOL'),('Bolivia','CONMEBOL'),('Brazil','CONMEBOL'),
('Chile','CONMEBOL'),('Colombia','CONMEBOL'),('Ecuador','CONMEBOL'),
('Paraguay','CONMEBOL'),('Peru','CONMEBOL'),('Uruguay','CONMEBOL'),
('Venezuela','CONMEBOL');

-- ---------------------------------------------------------------------------
-- CONCACAF (35)
-- ---------------------------------------------------------------------------
INSERT INTO fifa_teams (team_name, confederation) VALUES
('Anguilla','CONCACAF'),('Antigua and Barbuda','CONCACAF'),('Aruba','CONCACAF'),
('Bahamas','CONCACAF'),('Barbados','CONCACAF'),('Belize','CONCACAF'),
('Bermuda','CONCACAF'),('British Virgin Islands','CONCACAF'),('Canada','CONCACAF'),
('Cayman Islands','CONCACAF'),('Costa Rica','CONCACAF'),('Cuba','CONCACAF'),
('Curaçao','CONCACAF'),('Dominica','CONCACAF'),('Dominican Republic','CONCACAF'),
('El Salvador','CONCACAF'),('Grenada','CONCACAF'),('Guatemala','CONCACAF'),
('Guyana','CONCACAF'),('Haiti','CONCACAF'),('Honduras','CONCACAF'),
('Jamaica','CONCACAF'),('Mexico','CONCACAF'),('Montserrat','CONCACAF'),
('Nicaragua','CONCACAF'),('Panama','CONCACAF'),('Puerto Rico','CONCACAF'),
('Saint Kitts and Nevis','CONCACAF'),('Saint Lucia','CONCACAF'),
('Saint Vincent and the Grenadines','CONCACAF'),('Suriname','CONCACAF'),
('Trinidad and Tobago','CONCACAF'),('Turks and Caicos Islands','CONCACAF'),
('United States','CONCACAF'),('United States Virgin Islands','CONCACAF');

-- ---------------------------------------------------------------------------
-- CAF (54)
-- ---------------------------------------------------------------------------
INSERT INTO fifa_teams (team_name, confederation) VALUES
('Algeria','CAF'),('Angola','CAF'),('Benin','CAF'),('Botswana','CAF'),
('Burkina Faso','CAF'),('Burundi','CAF'),('Cameroon','CAF'),('Cape Verde','CAF'),
('Central African Republic','CAF'),('Chad','CAF'),('Comoros','CAF'),('Congo','CAF'),
('DR Congo','CAF'),('Djibouti','CAF'),('Egypt','CAF'),('Equatorial Guinea','CAF'),
('Eritrea','CAF'),('Eswatini','CAF'),('Ethiopia','CAF'),('Gabon','CAF'),
('Gambia','CAF'),('Ghana','CAF'),('Guinea','CAF'),('Guinea-Bissau','CAF'),
('Ivory Coast','CAF'),('Kenya','CAF'),('Lesotho','CAF'),('Liberia','CAF'),
('Libya','CAF'),('Madagascar','CAF'),('Malawi','CAF'),('Mali','CAF'),
('Mauritania','CAF'),('Mauritius','CAF'),('Morocco','CAF'),('Mozambique','CAF'),
('Namibia','CAF'),('Niger','CAF'),('Nigeria','CAF'),('Rwanda','CAF'),
('São Tomé and Príncipe','CAF'),('Senegal','CAF'),('Seychelles','CAF'),
('Sierra Leone','CAF'),('Somalia','CAF'),('South Africa','CAF'),
('South Sudan','CAF'),('Sudan','CAF'),('Tanzania','CAF'),('Togo','CAF'),
('Tunisia','CAF'),('Uganda','CAF'),('Zambia','CAF'),('Zimbabwe','CAF');

-- ---------------------------------------------------------------------------
-- AFC (46)
-- ---------------------------------------------------------------------------
INSERT INTO fifa_teams (team_name, confederation) VALUES
('Afghanistan','AFC'),('Australia','AFC'),('Bahrain','AFC'),('Bangladesh','AFC'),
('Bhutan','AFC'),('Brunei','AFC'),('Cambodia','AFC'),('China PR','AFC'),
('Taiwan','AFC'),('Guam','AFC'),('Hong Kong','AFC'),('India','AFC'),
('Indonesia','AFC'),('Iran','AFC'),('Iraq','AFC'),('Japan','AFC'),('Jordan','AFC'),
('Kuwait','AFC'),('Kyrgyzstan','AFC'),('Laos','AFC'),('Lebanon','AFC'),
('Macau','AFC'),('Malaysia','AFC'),('Maldives','AFC'),('Mongolia','AFC'),
('Myanmar','AFC'),('Nepal','AFC'),('North Korea','AFC'),('Oman','AFC'),
('Pakistan','AFC'),('Palestine','AFC'),('Philippines','AFC'),('Qatar','AFC'),
('Saudi Arabia','AFC'),('Singapore','AFC'),('South Korea','AFC'),('Sri Lanka','AFC'),
('Syria','AFC'),('Tajikistan','AFC'),('Thailand','AFC'),('Timor-Leste','AFC'),
('Turkmenistan','AFC'),('United Arab Emirates','AFC'),('Uzbekistan','AFC'),
('Vietnam','AFC'),('Yemen','AFC');

-- ---------------------------------------------------------------------------
-- OFC (11)
-- ---------------------------------------------------------------------------
INSERT INTO fifa_teams (team_name, confederation) VALUES
('American Samoa','OFC'),('Cook Islands','OFC'),('Fiji','OFC'),
('New Caledonia','OFC'),('New Zealand','OFC'),('Papua New Guinea','OFC'),
('Samoa','OFC'),('Solomon Islands','OFC'),('Tahiti','OFC'),('Tonga','OFC'),
('Vanuatu','OFC');

-- Sanity check: should return 211
-- SELECT COUNT(*) FROM fifa_teams;

-- ============================================================================
-- is_wc2026 : 2026 FIFA World Cup qualifiers
-- ----------------------------------------------------------------------------
-- (A) CONFIRMED as of Jan 2026 knowledge: 3 co-hosts + confederation slots
--     that were already decided. These I'm confident about.
-- ============================================================================
UPDATE fifa_teams SET is_wc2026 = 1 WHERE team_name IN (
    -- Hosts (automatic)
    'United States','Canada','Mexico',
    -- CONMEBOL direct
    'Argentina','Brazil','Uruguay','Ecuador','Colombia','Paraguay',
    -- AFC direct
    'Japan','Iran','South Korea','Australia','Jordan','Uzbekistan','Qatar','Saudi Arabia',
    -- OFC direct
    'New Zealand',
    -- CAF group winners (verify – CAF concluded after partial knowledge)
    'Morocco','Tunisia','Egypt','Algeria','Ghana','Cape Verde','South Africa',
    'Ivory Coast','Senegal'
);

-- ============================================================================
-- (B) TODO – complete the 48. The following slots concluded AFTER Jan 2026
--     and are NOT marked above (UEFA 16, CONCACAF 3 direct, and the
--     inter-confederation / intercontinental play-off winners). Fill in the
--     real qualifiers, then run:
--
--   UPDATE fifa_teams SET is_wc2026 = 1 WHERE team_name IN (
--       /* e.g. */ 'France','England','Spain','Portugal', ...
--   );
--
-- Verify the final count is exactly 48:
--   SELECT COUNT(*) FROM fifa_teams WHERE is_wc2026 = 1;
-- ============================================================================

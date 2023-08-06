BEGIN

CREATE OR REPLACE PROCEDURE HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.HANDLE_NEW_QUESTION_RUNS()
	returns string
	language javascript
	execute as owner as
	$$
        // Installs the handler for new question runs

        try {

            var crRequestSql = "SELECT id AS request_id, " +
            " request_data:clean_room_id AS clean_room_id, " +
            " request_data:result_table AS result_table, " +
            " request_data:result_table_ddl AS result_table_ddl, " +
            " request_data:accounts AS accounts, " +
            " request_data:accountNames AS accountNames, " +
            " request_data:organizationNames AS organizationNames, " +
            " request_data:compute_account_id AS compute_account_id, " +
            " request_data:statement_hash AS statement_hash, " +
            " request_data:question_run_query AS question_run_query " +
            " FROM HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.CLEAN_ROOM_REQUESTS " +
            " WHERE request_type = :1 AND request_status = :2 ORDER BY CREATED_AT ASC";

            var stmt = snowflake.createStatement({
                sqlText: crRequestSql,
                binds: ['NEW_QUESTION_RUN', 'PENDING']
            });

            var rs = stmt.execute();
            var newQuestionRunParams = [];
            while (rs.next()) {
                var requestID = rs.getColumnValue(1);
                var cleanRoomID = rs.getColumnValue(2);
                var resultTable = rs.getColumnValue(3);
                var resultTableDDL = rs.getColumnValue(4);
                var accounts = rs.getColumnValue(5);
                var accountNames = rs.getColumnValue(6);
                var organizationNames = rs.getColumnValue(7);
                var computeAccountId = rs.getColumnValue(8);
                var statementHash = rs.getColumnValue(9);
                var query = rs.getColumnValue(10);

                newQuestionRunParams.push({
                    'requestID' : requestID,
                    'cleanRoomID' : cleanRoomID,
                    'resultTable' : resultTable,
                    'resultTableDDL' : resultTableDDL,
                    'accounts' : accounts,
                    'accountNames': accountNames,
                    'organizationNames': organizationNames,
                    'computeAccountId': computeAccountId,
                    'statementHash': statementHash,
                    'query' : query
                })
                snowflake.execute({
                        sqlText: "UPDATE HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.CLEAN_ROOM_REQUESTS SET REQUEST_STATUS = :1, UPDATED_AT = CURRENT_TIMESTAMP() WHERE ID = :2",
                        binds: ["IN_PROGRESS", requestID]
                });
            }

            
            for (var i = 0; i < newQuestionRunParams.length; i++) {
                var stmt = snowflake.createStatement({
                    sqlText: 'CALL CLEAN_ROOM.ADD_NEW_QUESTION_RUN(:1, :2, :3, :4, :5, :6, :7, :8, :9, :10)',
                    binds: [
                        newQuestionRunParams[i]['requestID'],
                        newQuestionRunParams[i]['cleanRoomID'],
                        newQuestionRunParams[i]['resultTable'],
                        newQuestionRunParams[i]['resultTableDDL'],
                        newQuestionRunParams[i]['accounts'],
                        newQuestionRunParams[i]['accountNames'],
                        newQuestionRunParams[i]['organizationNames'],
                        newQuestionRunParams[i]['computeAccountId'],
                        newQuestionRunParams[i]['statementHash'],
                        newQuestionRunParams[i]['query']
                    ]
                });
                stmt.execute();
            }
            result = "SUCCESS";
        } catch (err) {
            
            result = "FAILED";
            var stmt = snowflake.createStatement({
                sqlText: 'CALL CLEAN_ROOM.HANDLE_ERROR(:1, :2, :3, :4, :5, :6)',
                binds: [
                    err.code, err.state, err.message, err.stackTraceTxt, "", Object.keys(this)[0]
                ]
            });
            var res = stmt.execute();
        }
        return result;
	$$;

CREATE OR REPLACE PROCEDURE HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.ADD_NEW_QUESTION_RUN(REQUEST_ID VARCHAR, CLEAN_ROOM_ID VARCHAR, RESULT_TABLE VARCHAR, RESULT_TABLE_DDL VARCHAR, ACCOUNTS_INPUT VARCHAR, ACCOUNT_NAMES_INPUT VARCHAR, ORG_NAMES_INPUT VARCHAR, COMPUTE_ACCOUNT_ID VARCHAR, STATEMENT_HASH VARCHAR, QUESTION_RUN_QUERY VARCHAR)
	returns string
	language javascript
	execute as owner as
	$$
        // Install the New question run stored procedure

        try {
            
            var sf_clean_room_id = CLEAN_ROOM_ID.replace(/-/g, '').toUpperCase();

            var habuShareDb = "HABU_CR_" + sf_clean_room_id + "_HABU_SHARE"

            snowflake.execute({
                sqlText: RESULT_TABLE_DDL
            });

            snowflake.execute({
                sqlText: "GRANT SELECT ON TABLE HABU_CLEAN_ROOM_" + sf_clean_room_id + ".CLEAN_ROOM_RUN_RESULTS." + RESULT_TABLE + " TO SHARE " + habuShareDb
            });

            if ((ACCOUNTS_INPUT != null && ACCOUNTS_INPUT.trim().length) != 0 &&
                (ACCOUNT_NAMES_INPUT != null && ACCOUNT_NAMES_INPUT.trim().length != 0) &&
                (ORG_NAMES_INPUT != null && ORG_NAMES_INPUT.trim().length != 0)
                ) {
                ACCOUNTS = ACCOUNTS_INPUT.split(",");
                ACCOUNT_NAMES = ACCOUNT_NAMES_INPUT.split(",");
                ORG_NAMES = ORG_NAMES_INPUT.split(",");
                for (var i = 0; i < ACCOUNTS.length; i++) {
                    var partnerShare = "HABU_CR_" + sf_clean_room_id + "_PARTNER_SHARE"
                    var partnerShareDb = "HABU_CR_" + ACCOUNTS[i] + "_" + sf_clean_room_id + "_PARTNER_SHARE_DB"
                    var shareName = ORG_NAMES[i] + "." + ACCOUNT_NAMES[i] + "." + partnerShare

                    snowflake.execute({
                        sqlText: "CREATE DATABASE IF NOT EXISTS " + partnerShareDb + " FROM SHARE " + shareName + " COMMENT = 'HABU_" + ACCOUNTS[i] + "'"
                    });

                    snowflake.execute({
                        sqlText: "GRANT IMPORTED PRIVILEGES ON DATABASE " + partnerShareDb + " TO ROLE ACCOUNTADMIN"
                    })
                    snowflake.execute({
                        sqlText: "GRANT IMPORTED PRIVILEGES ON DATABASE " + partnerShareDb + " TO ROLE SYSADMIN"
                    });
                }
            }

            snowflake.execute({
                sqlText: "INSERT INTO HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.ALLOWED_STATEMENTS (ACCOUNT_ID, CLEAN_ROOM_ID, STATEMENT_HASH) VALUES (:1, :2, :3)",
                binds: [COMPUTE_ACCOUNT_ID, CLEAN_ROOM_ID, STATEMENT_HASH]
            })

            // Execute the actual question query
            var resultSet = snowflake.execute({sqlText: QUESTION_RUN_QUERY})
            qId = Object.keys(this)[0] + " - QUESTION_RUN_QUERY - Query ID: " + resultSet.getQueryId()

            
            snowflake.createStatement({
                sqlText: 'CALL CLEAN_ROOM.SP_LOGGER(:1, :2, :3)',
                binds:[qId, REQUEST_ID, Object.keys(this)[0]]
            }).execute();

            snowflake.execute({
                sqlText: "DELETE FROM HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.ALLOWED_STATEMENTS where ACCOUNT_ID = :1 and CLEAN_ROOM_ID = :2 and STATEMENT_HASH = :3",
                binds: [COMPUTE_ACCOUNT_ID, CLEAN_ROOM_ID, STATEMENT_HASH]
            })

            result = "COMPLETE";
            msg = "New question run added successfully"
        } catch (err) {
            
            result = "FAILED";
            var stmt = snowflake.createStatement({
                sqlText: 'CALL CLEAN_ROOM.HANDLE_ERROR(:1, :2, :3, :4, :5, :6)',
                binds: [
                    err.code, err.state, err.message, err.stackTraceTxt, REQUEST_ID, Object.keys(this)[0]
                ]
            });
            msg = err.message
            var res = stmt.execute();
        } finally {
            snowflake.execute({
                sqlText: "UPDATE HABU_CLEAN_ROOM_COMMON.CLEAN_ROOM.CLEAN_ROOM_REQUESTS SET REQUEST_STATUS = :1, UPDATED_AT = CURRENT_TIMESTAMP() WHERE ID = :2",
                binds: [result, REQUEST_ID]
            });

            
            opMsg = Object.keys(this)[0] + " - OPERATION STATUS - " + result + " - Detail: " + msg
            snowflake.createStatement({
                sqlText: 'CALL CLEAN_ROOM.SP_LOGGER(:1, :2, :3)',
                binds:[opMsg, REQUEST_ID, Object.keys(this)[0]]
            }).execute();
        }
        return result;
	$$;


end;

